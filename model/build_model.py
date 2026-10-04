#!/usr/bin/env python3
"""Export the prepared layered art as a self-contained Halfne model script."""
from pathlib import Path
import argparse, base64, hashlib, json, math
import numpy as np
from PIL import Image
from mouth_vector_assets import create as create_mouth_assets

BASE=Path(__file__).resolve().parent

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--rig',type=Path,default=BASE.parent/'assets/gumi/rig_exports.json')
    ap.add_argument('--features',type=Path,default=BASE.parent/'audio_features.npz')
    ap.add_argument('--duration',type=float,default=234.05714583333334)
    ap.add_argument('--fps',type=int,default=60)
    args=ap.parse_args()
    rig=json.loads(args.rig.read_text()); parts=rig['parts']
    source_size=rig['canvas_size']; scale=520/source_size[1]
    by_id={p['id']:p for p in parts}
    body=by_id['body']; foot=body['pivot']
    data={}; geometry=[]
    for p in parts:
        src=(args.rig.parent/p['file']).resolve()
        im=Image.open(src).convert('RGBA')
        w,h=max(1,round(im.width*scale)),max(1,round(im.height*scale))
        im=im.resize((w,h),Image.Resampling.LANCZOS)
        texture=BASE/'source_parts'/f"{p['id']}.png"; texture.parent.mkdir(exist_ok=True)
        im.save(texture)
        data[p['id']]='data:image/png;base64,'+base64.b64encode(texture.read_bytes()).decode()
        parent=p.get('parent')
        pp=by_id[parent]['pivot'] if parent else foot
        position=p.get('crop_position',p.get('position',[0,0]))
        geometry.append({'id':p['id'],'parent':parent,'width':w,'height':h,
          'x':(p['pivot'][0]-pp[0])*scale,'y':(p['pivot'][1]-pp[1])*scale,
          'resourceCenterX':(p['pivot'][0]-position[0])*scale,
          'resourceCenterY':(p['pivot'][1]-position[1])*scale,
          'z':p.get('z',len(geometry)),'source_sha256':sha(src),'texture_sha256':sha(texture)})
    mouth_files,mouth_meta=create_mouth_assets(args.rig.parent/'parts/head.png',BASE/'mouth_assets')
    for name,source in mouth_files.items():
        im=Image.open(source).convert('RGBA');w,h=round(im.width*scale),round(im.height*scale)
        im=im.resize((w,h),Image.Resampling.LANCZOS)
        texture=BASE/'source_parts'/f'mouth_{name}.png';im.save(texture)
        data[f'mouth_{name}']='data:image/png;base64,'+base64.b64encode(texture.read_bytes()).decode()
    mouth_center=mouth_meta['global_mouth_center'];patch=mouth_meta['global_patch_box'];head=by_id['head']
    data['mouth']=data['mouth_closed']
    geometry.append({'id':'mouth','parent':'head','width':w,'height':h,
      'x':(mouth_center[0]-head['pivot'][0])*scale,'y':(mouth_center[1]-head['pivot'][1])*scale,
      'resourceCenterX':(mouth_center[0]-patch[0])*scale,'resourceCenterY':(mouth_center[1]-patch[1])*scale,
      'z':20,'source_sha256':sha(mouth_files['closed']),'texture_sha256':sha(BASE/'source_parts/mouth_closed.png')})
    # No external textures are needed when importing native-model.js.
    texture_js='const TEXTURES='+json.dumps(data,separators=(',',':'))+';\n'
    geometry_js='const PARTS='+json.dumps(geometry,separators=(',',':'))+';\n'
    geom={'source_canvas':source_size,'native_height':520,'scale':scale,'anchor':[400,560],
      'source_anchor':foot,'crop_box':[400-foot[0]*scale-18,560-foot[1]*scale-18,
           400+(source_size[0]-foot[0])*scale+18,560+(source_size[1]-foot[1])*scale+18]}
    controls={'mouse':'Head follows mouse gently; no face mesh distortion',
      'EyeBlink / x':'Hold to close eyes','EyeHappy / 1':'Calm idle',
      'EyeJaded / 2':'Slightly stronger sway','Wave':'Small hand wave in imported actions',
      'MouthAA / a':'Large open mouth','MouthEE / d':'Medium mouth','MouthOO / w':'Rounded mouth',
      'MouthEH / s':'Small open mouth','MouthOH / e':'Large rounded mouth',
      'mouthOpen':'Recorded vocal-activity opening 0..1; pauses closed',
      'animationTime':'Optional deterministic playback clock in seconds',
      'audioEnergy':'Optional music energy 0..1; subtle amplitude only'}
    code='''// GUMI big-head pencil chibi. Self-contained Halfne Miku Studio Reborn model.
// Settings tab -> Import Model. Assets below are embedded PNG data URLs.
// Actual importer calls mikuConfig(); do not add an ES module export.
'''+texture_js+geometry_js+'''
const clamp=(v,l,h)=>Math.max(l,Math.min(h,v));
const s=(t,p,phase=0)=>Math.sin(t*Math.PI*2/p+phase);
const blinkCenters=[2.5,6.9,11.8,17.4,22.6,28.9,34.1,40.3,46.8,52.1,57.9,64.3,70.4,75.9,81.6,86.9,93.0,99.5,105.1,111.8,117.3,123.1,129.8,135.3,141.1,147.3,154.8,160.9,167.2,173.8,179.4,185.7,191.5,197.6,204.1,210.6,216.3,223.1,230.2];
const mikuConfig=()=>{
  const nodes={};
  let normalize;
  let lastSeenLiveTimestamp;
  const pathOf=id=>{const p=PARTS.find(o=>o.id===id);return p.parent?pathOf(p.parent)+'.'+id:id};
  PARTS.forEach(p=>{
    const n={id:p.id,x:p.x,y:p.y,rotation:0,scaleX:1,scaleY:1,
      width:p.width,height:p.height,resourceCenterX:p.resourceCenterX,
      resourceCenterY:p.resourceCenterY,resource:TEXTURES[p.id],components:[]};
    if(p.id==='body') {
      n.x=c=>p.x+1.35*s(c.time,8.5);
      n.y=c=>p.y-1.75*(.5+.5*s(c.time,4.8));
      n.rotation=c=>(.35*s(c.time,6.5)+.12*Math.sin(c.time*.73))*(.9+.2*c.audioEnergy)+c.lookX*.65;
    } else if(p.id==='head') {
      n.y=c=>p.y+c.lookY*1.8;
      n.rotation=c=>1.1*s(c.time,5.9,1.1)+c.lookX*1.9;
    } else if(p.id.startsWith('hair_')||p.id==='skirt') {
      const isSkirt=p.id==='skirt';
      n.massX=0;n.massY=isSkirt?35:46;
      n.gravityX=c=>(isSkirt?.000014:.000023)*Math.sin(c.time*.8+(p.id==='hair_right'?1.7:.2));
      n.gravityY=.0009;n.damp=.005;
      n.rotationMin=isSkirt?-1.7:-2.2;n.rotationMax=isSkirt?1.7:2.2;
      n.rotation=physicsRotation(pathOf(p.id));
    } else if(p.id.startsWith('arm_')) {
      const right=p.id==='arm_right';
      n.rotation=c=>(right?.9:-.8)*s(c.time,right?5.4:4.9,right?1.4:.3)*(c.mode===2?1.35:1)
        +(right?-1:1)*c.wave*1.1*(.5+.5*s(c.time,1.3));
    } else if(p.id.startsWith('eye_')||p.id==='eyes') {
      n.opacity=c=>c.blink>=.5?1:0;
    } else if(p.id==='mouth') {
      n.resource=c=>TEXTURES['mouth_'+(c.mouthOpen<.10?'closed':c.mouthKind==='round'?'round':
        c.mouthOpen<.30?'small':c.mouthOpen<.50?'medium':c.mouthOpen<.74?'wide':'large')];
    }
    // Importing during live playback can briefly retain the Studio's previous
    // parser closure. Tolerate its raw/default-model controls on every callback.
    for(const k of Object.keys(n))if(typeof n[k]==='function') {
      const fn=n[k];n[k]=(control,root,physics)=>fn(normalize(control),root,physics);
    }
    nodes[p.id]=n;
  });
  const roots=[];
  [...PARTS].sort((a,b)=>a.z-b.z).forEach(p=>{
    if(p.parent) nodes[p.parent].components.push(nodes[p.id]);else roots.push(nodes[p.id]);
  });
  const config={
    background:{Paper:'#F7F4EC',Blue:'#EDF2F5'},
    defaultKeyMapping:[['EyeBlink','x'],['EyeHappy','1'],['EyeJaded','2'],
      ['MouthAA','a'],['MouthEE','d'],['MouthOO','w'],['MouthEH','s'],['MouthOH','e']],
    metadata:{geometry:GEOMETRY,controls:CONTROLS,resourceCatalog:TEXTURES,mouth:MOUTH_GEOMETRY},
    parseControl:(input={})=>{
      const c={mouseX:400,mouseY:300,keyInput:[],mode:1,audioEnergy:0,...input};
      // The Studio preserves parsed fields between updates. A new live
      // timestamp must release a previously imported recording clock.
      const previousStamp=Number.isFinite(lastSeenLiveTimestamp)?lastSeenLiveTimestamp:c._lastTimestamp;
      const liveClock=Number.isFinite(c.timestamp)&&(Number.isFinite(previousStamp)?
        c.timestamp!==previousStamp:!Number.isFinite(c.animationTime));
      if(liveClock){c.time=c.timestamp/1000;delete c.animationTime;}
      else c.time=Number.isFinite(c.animationTime)?c.animationTime:
        Number.isFinite(c.timestamp)?c.timestamp/1000:(Number.isFinite(c.time)?c.time+1/60:0);
      if(Number.isFinite(c.timestamp)){c._lastTimestamp=c.timestamp;lastSeenLiveTimestamp=c.timestamp;}
      c.lookX=clamp(Math.atan((c.mouseX-400)/400)*2/Math.PI,-1,1);
      c.lookY=clamp(Math.atan((c.mouseY-300)/300)*2/Math.PI,-1,1);
      c.audioEnergy=clamp(Number(c.audioEnergy)||0,0,1);
      c.wave=0;
      if(c.keyInput.includes('EyeHappy')||c.keyInput.includes('Idle'))c.mode=1;
      if(c.keyInput.includes('EyeJaded')||c.keyInput.includes('Sway'))c.mode=2;
      if(c.keyInput.includes('Wave'))c.wave=1;
      c.mouthOpen=liveClock?0:clamp(Number(c.mouthOpen)||0,0,1);c.mouthKind='open';
      if(c.keyInput.includes('MouthAA'))c.mouthOpen=.96;
      if(c.keyInput.includes('MouthEE'))c.mouthOpen=.44;
      if(c.keyInput.includes('MouthEH'))c.mouthOpen=.25;
      if(c.keyInput.includes('MouthOO')){c.mouthOpen=.70;c.mouthKind='round';}
      if(c.keyInput.includes('MouthOH')){c.mouthOpen=.96;c.mouthKind='round';}
      if(Number.isFinite(c.mouthOverride))c.mouthOpen=clamp(c.mouthOverride,0,1);
      c.voiced=!!c.voiced;
      const clock=((c.time%234.05714583333334)+234.05714583333334)%234.05714583333334;
      const d=Math.min(...blinkCenters.map(t=>Math.abs(clock-t)));
      const b=clamp((.135-d)/.11,0,1);c.blink=b*b*(3-2*b);
      if(c.keyInput.includes('EyeBlink'))c.blink=1;
      if(Number.isFinite(c.blinkOverride))c.blink=clamp(c.blinkOverride,0,1);
      return c;
    },
    model:{id:'root',x:400,y:560,rotation:0,scaleX:1,scaleY:1,components:roots}
  };
  const normalizedControls=new WeakMap();
  normalize=(input={})=>{
    const fields=['time','lookX','lookY','audioEnergy','blink','wave','mode','mouthOpen'];
    if(fields.every(k=>Number.isFinite(input[k]))&&
      (!Number.isFinite(input.timestamp)||input.timestamp===input._lastTimestamp))return input;
    // One consistent result per raw control object, shared by all components.
    if(normalizedControls.has(input))return normalizedControls.get(input);
    const value=config.parseControl(input);normalizedControls.set(input,value);return value;
  };
  return config;
};
'''
    # Metadata outside the model tree does not participate in native evaluation.
    code=code.replace('const mikuConfig=()=>{','const GEOMETRY='+json.dumps(geom,separators=(',',':'))+';\nconst CONTROLS='+json.dumps(controls,separators=(',',':'))+';\nconst MOUTH_GEOMETRY='+json.dumps(mouth_meta,separators=(',',':'))+';\nconst mikuConfig=()=>{')
    (BASE/'native-model.js').write_text(code)
    n=math.ceil(args.duration*args.fps); times=np.arange(n)/args.fps
    features=np.load(args.features);ft=features['times'];fe=features['energy']
    energy=np.interp(times,ft,fe)
    mouth_envelope=json.loads((BASE/'vocal_mouth_envelope.json').read_text())
    assert mouth_envelope['frame_count']==n and mouth_envelope['fps']==args.fps
    a=[]
    for i,t in enumerate(times):
      # Gentle editorial control curve. It can also be edited in the Studio.
      mouseX=400+45*math.sin(t*.31)+15*math.sin(t*.71)
      mouseY=300+26*math.sin(t*.24+.8)
      key=['EyeJaded'] if 121.68<=t<176.77 else ['EyeHappy']
      if 77.24<=t<79.24 or 209.0<=t<211.0:key.append('Wave')
      a.append({'t':float(i*1000/args.fps),'c':{'mouseX':mouseX,'mouseY':mouseY,'keyInput':key,
        'animationTime':float(t),'audioEnergy':float(energy[i]),
        'mouthOpen':mouth_envelope['mouthOpen'][i],'voiced':mouth_envelope['voiced'][i]}})
    (BASE/'HMSR_GUMI_PV.json').write_text(json.dumps([{'a':a,'v':True,'l':False}],separators=(',',':')))
    (BASE/'rig_exports.json').write_text(json.dumps(rig,ensure_ascii=False,indent=2))
    (BASE/'build_provenance.json').write_text(json.dumps({'rig_sha256':sha(args.rig),
       'audio_features_sha256':sha(args.features),'builder_sha256':sha(__file__),
       'vocal_mouth_envelope_sha256':sha(BASE/'vocal_mouth_envelope.json'),
       'source_geometry':geometry,'model_sha256':sha(BASE/'native-model.js')},indent=2))
    print(json.dumps({'native_js':str(BASE/'native-model.js'),'sha256':sha(BASE/'native-model.js'),'parts':len(parts),'frames':n}))

if __name__=='__main__':main()
