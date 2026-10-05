#!/usr/bin/env python3
"""Embed the PNG resources into the Studio-importable model (stdlib only)."""
from pathlib import Path
import argparse, base64, hashlib, json

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=ROOT / 'model/GUMI-Chibi-HMSR.js')
    parser.add_argument('--verify', action='store_true', help='Verify the release reference hash without writing')
    args = parser.parse_args()
    config = json.loads((ROOT / 'source/model-config.json').read_text(encoding='utf-8'))
    textures = {}
    for name, rel in config['textures'].items():
        asset = ROOT / 'source' / rel
        textures[name] = 'data:image/png;base64,' + base64.b64encode(asset.read_bytes()).decode('ascii')
    template = (ROOT / 'source/runtime.js').read_text(encoding='utf-8')
    if template.count('__EMBEDDED_TEXTURES__') != 1:
        raise SystemExit('The runtime template must have one texture placeholder')
    code = template.replace('__EMBEDDED_TEXTURES__', 'const TEXTURES=' + json.dumps(textures, separators=(',', ':')) + ';')
    data = code.encode('utf-8')
    digest = hashlib.sha256(data).hexdigest()
    if args.verify:
        if digest != config['expected_model_sha256']:
            raise SystemExit('Rebuilt model differs from the v1.0.0 reference')
        print('PASS: source rebuild matches the release model SHA-256')
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(data)
        print('Built', args.output.name, digest)

if __name__ == '__main__':
    main()
