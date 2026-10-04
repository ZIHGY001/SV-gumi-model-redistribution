#!/usr/bin/env node
// Load the exported single-file model through the real Halfne importer and
// resolve animation using its actual frame/physics engine. No npm packages.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {parseModelJS} from './upstream_runtime/modelUtils.mjs';
import {parseConfig, getInitPhysics, work} from './upstream_runtime/core.mjs';
import {getRawControl} from './upstream_runtime/App-control.mjs';

const HERE=path.dirname(fileURLToPath(import.meta.url));
const args=process.argv.slice(2), opts={};
for(let i=0;i<args.length;i++) {
  if(!args[i].startsWith('--')) throw new Error('Expected --option');
  opts[args[i].slice(2)]=args[i+1]&&!args[i+1].startsWith('--')?args[++i]:true;
}
const modelFile=path.resolve(opts.model||path.join(HERE,'native-model.js'));
const controlFile=path.resolve(opts.controls||path.join(HERE,'HMSR_GUMI_PV.json'));
const outFile=path.resolve(opts.output||path.join(HERE,'sampled_frames.json'));
const fps=Number(opts.fps||60), duration=Number(opts.duration||234.05714583333334);
const count=Math.ceil(duration*fps);
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const modelBytes=fs.readFileSync(modelFile), controlBytes=fs.readFileSync(controlFile);
const cfg=parseModelJS(modelBytes.toString('utf8'));
if(!cfg.model||typeof cfg.parseControl!=='function') throw new Error('Invalid imported Config');
const record=JSON.parse(controlBytes);
if(!Array.isArray(record)||!record.every(x=>Array.isArray(x.a))) throw new Error('Invalid Studio record format');
const probeIndices=opts.probe?new Set(String(opts.probe).split(',').map(Number)):null;
const limit=probeIndices?Math.max(...probeIndices)+1:count;
if(limit>count) throw new Error('Probe exceeds duration');
const resources=[], resourceMap=new Map(), parts=[];
const assetDir=path.join(HERE,'native_assets');
if(!probeIndices) fs.mkdirSync(assetDir,{recursive:true});
function resourceIndex(src) {
  if(!src) return -1;
  if(resourceMap.has(src)) return resourceMap.get(src);
  if(!src.startsWith('data:image/png;base64,')) throw new Error('A model texture is not an embedded PNG');
  const bytes=Buffer.from(src.split(',')[1],'base64'), hash=sha(bytes);
  const idx=resources.length, filename=`native_assets/${hash.slice(0,24)}.png`;
  resources.push({file:filename,sha256:hash,bytes:bytes.length});
  resourceMap.set(src,idx);
  if(!probeIndices) fs.writeFileSync(path.join(HERE,filename),bytes);
  return idx;
}
// Stable resource indices also include mouth shapes not selected at frame zero.
for(const src of Object.values(cfg.metadata.resourceCatalog||{}))resourceIndex(src);
function flatten(node,parent=-1,currentPath='',output=[]) {
  if(node.virtual) return output;
  const idx=output.length;
  const entry={id:node.id,path:currentPath,parent,width:node.width||0,height:node.height||0,
    resourceCenterX:node.resourceCenterX||0,resourceCenterY:node.resourceCenterY||0};
  output.push({entry,state:[node.x||0,node.y||0,node.rotation||0,
    node.scaleX===undefined?1:node.scaleX,node.scaleY===undefined?1:node.scaleY,
    node.opacity===undefined?1:node.opacity,resourceIndex(node.resource)]});
  for(const child of node.components||[]) flatten(child,idx,currentPath?`${currentPath}.${child.id}`:child.id,output);
  return output;
}
let control=cfg.parseControl({...getRawControl(record,0),animationTime:0});
let physics=getInitPhysics(parseConfig(cfg.model,control));
const frames=[], controls=[], probes=[];
let maximumRotation=0;
for(let i=0;i<limit;i++) {
  const t=i/fps;
  // Match App.js export's multiplication/division order exactly; otherwise
  // binary floating-point may select the previous recorded control frame.
  const raw=getRawControl(record,i*1000/fps);
  // The record's animationTime is the production clock, not wall-clock time.
  raw.animationTime=t;
  if(opts['blink-override']!==undefined) raw.blinkOverride=Number(opts['blink-override']);
  if(opts['mouth-override']!==undefined) raw.mouthOverride=Number(opts['mouth-override']);
  control=cfg.parseControl({...control,...raw});
  let resolved;
  work(i===0?0:1000/fps,cfg.model,control,physics,p=>{physics=p},r=>{resolved=r},true);
  const flat=flatten(resolved);
  if(i===0) parts.push(...flat.map(x=>x.entry));
  if(flat.length!==parts.length||flat.some((x,j)=>x.entry.path!==parts[j].path)) throw new Error('Animated hierarchy is not stable');
  const states=flat.map(x=>x.state);
  if(states.some(a=>a.some(x=>!Number.isFinite(x)))) throw new Error(`Non-finite frame ${i}`);
  states.forEach(a=>{maximumRotation=Math.max(maximumRotation,Math.abs(a[2]))});
  const con=[t,control.lookX,control.lookY,control.audioEnergy,control.blink,control.mode,control.wave,control.mouthOpen,Number(control.voiced)];
  if(probeIndices) {
    if(probeIndices.has(i)) probes.push({frame:i,states,control:con,physics:structuredClone(physics)});
  } else {frames.push(states);controls.push(con)}
}
const runtimeManifest=JSON.parse(fs.readFileSync(path.join(HERE,'upstream_runtime/upstream_source_manifest.json')));
for(const item of runtimeManifest) {
  if(sha(fs.readFileSync(path.join(HERE,item.runtime_file)))!==item.runtime_sha256) throw new Error(`Changed upstream runtime: ${item.runtime_file}`);
}
const result={schema:'halfne-native-samples-v1',fps,frame_count:count,duration,stage:[800,600],
  model_js_sha256:sha(modelBytes),control_file_sha256:sha(controlBytes),
  runtime_sha256:Object.fromEntries(runtimeManifest.map(x=>[x.runtime_file,x.runtime_sha256])),
  sampler_sha256:sha(fs.readFileSync(fileURLToPath(import.meta.url))),
  frame_schema:['x','y','rotation','scaleX','scaleY','opacity','resourceIndex'],
  control_schema:['time','lookX','lookY','audioEnergy','blink','mode','wave','mouthOpen','voiced'],
  geometry:cfg.metadata.geometry,mouth_geometry:cfg.metadata.mouth,parts,resources};
if(probeIndices) {
  process.stdout.write(JSON.stringify({...result,probes})+'\n');
} else {
  fs.writeFileSync(outFile,JSON.stringify({...result,frames,controls}));
  fs.writeFileSync(path.join(HERE,'native_assets.json'),JSON.stringify({model_js_sha256:result.model_js_sha256,resources},null,2));
  const controlManifest={schema:'halfne-native-controls-v1',record:'HMSR_GUMI_PV.json',
    record_sha256:sha(controlBytes),fps,frame_count:count,duration,
    clock:'animationTime seconds, frame index / fps',
    raw_control_reader:'upstream_runtime/App-control.mjs',
    raw_control_reader_sha256:sha(fs.readFileSync(path.join(HERE,'upstream_runtime/App-control.mjs'))),
    controls:cfg.metadata.controls};
  fs.writeFileSync(path.join(HERE,'control_manifest.json'),JSON.stringify(controlManifest,null,2));
  const fileBinding=p=>({path:p,sha256:sha(fs.readFileSync(path.join(HERE,p)))});
  const manifest={schema:'halfne-native-model-v1',native_js:fileBinding('native-model.js'),
    sample_file:fileBinding(path.relative(HERE,outFile)),control_manifest:fileBinding('control_manifest.json'),
    actions:fileBinding('HMSR_GUMI_PV.json'),sampler:fileBinding('sample_native_model.mjs'),
    assets_manifest:fileBinding('native_assets.json'),mouth_envelope:fileBinding('vocal_mouth_envelope.json'),upstream_runtime:runtimeManifest,
    frame_count:count,fps,geometry:cfg.metadata.geometry};
  fs.writeFileSync(path.join(HERE,'model_manifest.json'),JSON.stringify(manifest,null,2));
  process.stdout.write(JSON.stringify({passed:true,importer:'upstream parseModelJS',engine:'upstream work/getInitPhysics',
    frame_count:count,parts:parts.length,resources:resources.length,maximumRotation,
    model_js_sha256:result.model_js_sha256,sample_file_sha256:sha(fs.readFileSync(outFile)),
    control_manifest_sha256:sha(fs.readFileSync(path.join(HERE,'control_manifest.json'))),output:outFile})+'\n');
}
