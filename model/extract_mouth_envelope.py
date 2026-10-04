"""Approximate singing activity from the delivered mix and unchanged lyric anchors.

This is deliberately not a phoneme recognizer or a stem separator. A centre-
weighted voice band, with an instrumental spectral floor removed, supplies
amplitude; existing audio-aligned word windows supply the singing/pause gate.
Nothing from the low-frequency music visualizer is used to open the mouth.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess
import numpy as np
from scipy import ndimage, signal

ROOT = Path(__file__).resolve().parents[1]
SOURCE_SHA = '04f3d5f71e06df8105f76c088ef30bb4e449399871dd7861441c650ce7d4a9c3'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def intervals(mask, fps):
    a = np.flatnonzero(np.diff(np.r_[False, mask, False].astype(np.int8)))
    return [[round(float(l/fps), 6), round(float(r/fps), 6)] for l, r in a.reshape(-1, 2)]


def analyze(source, timeline_path, output):
    timeline = json.loads(timeline_path.read_text())
    if sha(source) != SOURCE_SHA:
        raise ValueError('Use the unchanged latest de-essed user MP3')
    pcm = subprocess.check_output(['ffmpeg', '-hide_banner', '-v', 'error', '-nostdin',
        '-i', str(source), '-f', 'f32le', '-ar', '16000', '-ac', '2', 'pipe:1'])
    audio = np.frombuffer(pcm, np.float32).reshape(-1, 2)
    sample_rate, hop = 16000, 160
    centre = audio.mean(axis=1)
    side = (audio[:,0]-audio[:,1])*.5
    freq, times, mid_stft = signal.stft(centre, sample_rate, nperseg=1024,
        noverlap=1024-hop, boundary='zeros')
    _, _, side_stft = signal.stft(side, sample_rate, nperseg=1024,
        noverlap=1024-hop, boundary='zeros')
    # Mid-side reduction suppresses wide-panned accompaniment. Bass/drum energy
    # below 300 Hz never enters the mouth control. This is only an estimate.
    band = (freq >= 300) & (freq <= 3500)
    centre_power = np.abs(mid_stft[band])**2
    side_power = np.abs(side_stft[band])**2
    spectral_power = np.maximum(centre_power - .45*side_power, 0)
    instrumental = np.zeros(len(times), bool)
    for item in timeline['instrumental']:
        instrumental |= (times >= item['start']) & (times < item['end'])
    # Frequency-wise accompaniment floor is derived ONLY from documented
    # instrumental passages, not from imagined silent sections in lyrics.
    floor = np.percentile(spectral_power[:,instrumental], 60, axis=1)
    residual = np.maximum(spectral_power - floor[:,None]*.85, 0)
    # Weight vocal/formant range. Sibilance above 3.5 kHz cannot trigger mouth.
    weights = np.interp(freq[band], [300,500,1200,2200,3500], [.4,.85,1,1,.35])
    band_rms = np.sqrt((residual*weights[:,None]).sum(axis=0))
    band_rms = ndimage.gaussian_filter1d(band_rms, 1.4)
    fps = 60
    frame_count = math.ceil(float(timeline['duration'])*fps)
    clock = np.arange(frame_count)/fps
    rms = np.interp(clock, times, band_rms)
    phrase_gate = np.zeros(frame_count, bool)
    cue_gate = np.zeros(frame_count, bool)
    guard_windows = []
    punctuation_pauses = []
    pause_chars = set(' \u3000、，,。.!！?？\n')
    for number, cue in enumerate(timeline['events'], 1):
        cue_gate |= (clock >= cue['start']) & (clock < cue['end'])
        words = cue.get('words', [])
        if not words:
            raise ValueError('Expected preserved audio-aligned word anchors')
        for word in words:
            start, end = float(word['start']), float(word['end'])
            if not word['text'].strip() or all(x in pause_chars for x in word['text']):
                if end-start >= .12:
                    punctuation_pauses.append({'cue':number,'text':word['text'],
                        'start':start,'end':end})
                continue
            # A bounded release supports sustained vowels at an ASR end anchor.
            # It never extends into another cue/instrumental or over a long pause.
            left = max(float(cue['start']), start-.035)
            right = min(float(cue['end']), end+.10)
            phrase_gate |= (clock >= left) & (clock < right)
            guard_windows.append({'cue':number,'text':word['text'],
                'start':round(left,6),'end':round(right,6)})
    instrumental_frames = np.zeros(frame_count, bool)
    for item in timeline['instrumental']:
        instrumental_frames |= (clock >= item['start']) & (clock < item['end'])
    phrase_gate &= cue_gate & ~instrumental_frames
    for p in punctuation_pauses:
        # Preserve vowel release at the beginning; central pause stays closed.
        phrase_gate[(clock >= p['start']+.10) & (clock < p['end']-.035)] = False
    mouth = np.zeros(frame_count, np.float64)
    normalization = []
    for number, cue in enumerate(timeline['events'], 1):
        frames = (clock >= cue['start']) & (clock < cue['end']) & phrase_gate
        values = rms[frames]
        if not len(values): continue
        low, high = np.percentile(values, [12,88])
        if high-low < 1e-8: high = low+1e-8
        activity = np.clip((rms-low*.70)/(high-low*.70), 0, 1)
        # Moderate dynamic range retains long vowels while leaving real dips
        # and amplitude pauses visible. No arbitrary periodic jaw animation.
        activity = np.where(activity > .19, .18+.78*activity**.65, 0)
        mouth[frames] = activity[frames]
        normalization.append({'cue':number,'low':float(low),'high':float(high)})
    # Attack/release in seconds, followed by a hard gate. No instrumental tail.
    smoothed = np.zeros_like(mouth)
    for i,value in enumerate(mouth):
        prev = smoothed[i-1] if i else 0
        tau = .025 if value > prev else .045
        amount = 1-math.exp(-1/(fps*tau))
        smoothed[i] = prev+(value-prev)*amount
    smoothed[~phrase_gate] = 0
    smoothed[smoothed < .12] = 0
    mouth = np.round(smoothed, 5)
    voiced = mouth > 0
    data = {'schema':'halfne-vocal-activity-mouth-v1','fps':fps,
        'frame_count':frame_count,'duration':frame_count/fps,
        'source_mp3':'../../upload/'+source.name,'source_mp3_sha256':sha(source),
        'lyric_timeline_sha256':sha(timeline_path),'source_type':'stereo final mix; no isolated vocal supplied',
        'method':'centre-minus-side 300–3500 Hz STFT energy minus instrumental spectral floor; unchanged audio-aligned sung-word windows and punctuation pauses; attack/release smoothing',
        'phoneme_recognition':False,'separated_vocal_stem':False,
        'low_frequency_music_energy_used':False,'fps_clock':'frame_index / 60 seconds',
        'mouthOpen':mouth.tolist(),'voiced':voiced.tolist(),'phraseGate':phrase_gate.tolist(),
        'instrumental':timeline['instrumental'],'guard_windows':guard_windows,
        'punctuation_pause_windows':punctuation_pauses,'normalization':normalization,
        'closed_intervals':intervals(~voiced, fps),
        'analysis':{'sampling_rate':sample_rate,'stft_window':1024,'stft_hop':hop,
            'voice_band_hz':[300,3500],'side_subtraction':.45,
            'instrumental_floor_percentile':60,'instrumental_floor_multiplier':.85,
            'attack_seconds':.025,'release_seconds':.045,
            'frame_count':frame_count,'voiced_frames':int(voiced.sum()),
            'instrumental_frames':int(instrumental_frames.sum()),
            'instrumental_open_frames':int(voiced[instrumental_frames].sum()),
            'outside_lyric_open_frames':int(voiced[~cue_gate].sum()),
            'outside_phrase_guard_open_frames':int(voiced[~phrase_gate].sum())}}
    if any(data['analysis'][k] for k in ['instrumental_open_frames','outside_lyric_open_frames','outside_phrase_guard_open_frames']):
        raise ValueError('Mouth gate leaked into an instrumental/pause')
    output.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':')))
    np.savez_compressed(output.with_suffix('.npz'), t=clock, mouthOpen=mouth,
        phraseGate=phrase_gate, voiced=voiced, bandRMS=rms)
    print(json.dumps({'output':str(output),'sha256':sha(output),'analysis':data['analysis']},ensure_ascii=False,indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source',type=Path,default=ROOT.parent/'upload/プレイシック(1).mp3')
    parser.add_argument('--timeline',type=Path,default=ROOT/'lyrics_timeline.json')
    parser.add_argument('--output',type=Path,default=ROOT/'model/vocal_mouth_envelope.json')
    args = parser.parse_args()
    analyze(args.source,args.timeline,args.output)
