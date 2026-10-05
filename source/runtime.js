// GUMI big-head pencil chibi. Self-contained Halfne Miku Studio Reborn model.
// Settings tab -> Import Model. Assets below are embedded PNG data URLs.
// Actual importer calls mikuConfig(); do not add an ES module export.
__EMBEDDED_TEXTURES__
const PARTS=[{"id":"body","parent":null,"width":294,"height":374,"x":0.0,"y":0.0,"resourceCenterX":152.75773584905662,"resourceCenterY":349.86264150943396,"z":0,"source_sha256":"5702733402d2011062293e57d6ff8d7c58d60d47bc55dfddc657388a7cdf9aea","texture_sha256":"03623620c5fab22a0b85e98066b17a7c3ba8a35225853207664599f67410ff5c"},{"id":"skirt","parent":"body","width":187,"height":93,"x":-12.552452830188685,"y":-146.07018867924526,"resourceCenterX":88.12981132075471,"resourceCenterY":16.62264150943399,"z":1,"source_sha256":"a744361021d051ec8b34dd8af0f8ce9b203a0103ed0050473ff41b1762e3891b","texture_sha256":"93211b3a73f3be17ef71b7932ae3d46a6fadb537b8b3034c7a0eea605adcd3e9"},{"id":"arm_left","parent":"body","width":106,"height":120,"x":-56.137358490566044,"y":-193.14264150943396,"resourceCenterX":81.52603773584906,"resourceCenterY":20.870943396226412,"z":2,"source_sha256":"042c9ab822afce3cf8317b724abaf449af890b660c3223d5864474aaa6cc2399","texture_sha256":"4ddf1c31838a1bb98afd5f2be185a69dca564160e84a12bfdd2168d818663940"},{"id":"arm_right","parent":"body","width":96,"height":123,"x":49.163773584905705,"y":-193.14264150943396,"resourceCenterX":21.544150943396264,"resourceCenterY":17.85207547169811,"z":3,"source_sha256":"7dd0f9158de089ff23e4ed84f8e671919cd79f13dcd37ec4e19d4a9cf6ea7f6c","texture_sha256":"dffcdad32f7805a1191d06a9b9280cae2c9145af1cdc8474d759c6879ded5934"},{"id":"head","parent":"body","width":373,"height":292,"x":-6.624905660377374,"y":-204.78943396226413,"resourceCenterX":194.43471698113208,"resourceCenterY":280.9222641509434,"z":4,"source_sha256":"9eeb65721590cb9ddb95a20ade871a3bffb1fe12e63ab43dc7673d0a6ed0a400","texture_sha256":"7f9de09656d10f0bc7e65e57e8c7080f6d5a1296542653bea286774d06343cdb"},{"id":"hair_left","parent":"head","width":122,"height":217,"x":-85.77509433962261,"y":-69.39547169811327,"resourceCenterX":104.131320754717,"resourceCenterY":103.60226415094338,"z":5,"source_sha256":"b650dd85e14a66befdbfb5c8b227016690ae018ad8fa853d49aad7189e8a06b0","texture_sha256":"7031e73da225a2e4c3836ef60809f0b409caef13b165f3b9c05ce3f914815a5a"},{"id":"hair_right","parent":"head","width":127,"height":210,"x":73.222641509434,"y":-40.76377358490571,"resourceCenterX":26.1479245283019,"resourceCenterY":99.78113207547169,"z":6,"source_sha256":"607456bd03648928caeb886aa3e42677260e4097f05bd7d8b66e752b450264ee","texture_sha256":"60464d5be3e57f3e5c357c212710e07888fdaaf26b96cc1488c002271e5811eb"},{"id":"eye_left","parent":"head","width":49,"height":63,"x":-47.64226415094338,"y":-81.29962264150947,"resourceCenterX":24.528301886792455,"resourceCenterY":31.320754716981135,"z":7,"source_sha256":"1faf76744f0a4c0ee796bf15d6fbc42e9415133d66b3b26e0deb1873590508fb","texture_sha256":"a112b7443b670bde6752e961c8d74c5ab8705e7d1056a7ea74537dd5a96c430c"},{"id":"eye_right","parent":"head","width":54,"height":66,"x":50.84830188679248,"y":-68.46943396226419,"resourceCenterX":27.169811320754718,"resourceCenterY":32.83018867924528,"z":8,"source_sha256":"152267b5f6d938d5ed7308f13a84e2a9714299080c3d2c74288b4a9d46ba19bb","texture_sha256":"96f76c33b59583dedc46170b38555bbb681dee6d080433ed88e3deea6180cee3"},{"id":"mouth","parent":"head","width":35,"height":27,"x":-5.75547169811319,"y":-40.92226415094343,"resourceCenterX":16.60377358490566,"resourceCenterY":11.320754716981133,"z":20,"source_sha256":"1580af589fca823f265a091603db619b836ccfe79be0180ed550c67b6ded67cd","texture_sha256":"647bef18bd207e1b4bfb9db5c734ad4f43e209ed33ca543f2e0e03f9582d4e7a"},{"id":"expression_face","parent":"head","width":137,"height":105,"x":-2.736603773584888,"y":-94.12981132075475,"resourceCenterX":68.67924528301887,"resourceCenterY":52.45283018867925,"z":19,"source_sha256":"ecb74cbce2e72db979b723e8a561343eee5075a1720a171b0599abc1bfef40a7","texture_sha256":"51eeffb946ade0272bf78b4ab535cb00cc8ec2f228d1b782cf5151b5cae0256b"},{"id":"rear_hair_follow","parent":null,"width":275,"height":191,"x":-6.624905660377374,"y":-204.78943396226413,"resourceCenterX":139.34037735849057,"resourceCenterY":134.50716981132078,"z":-1,"source_sha256":"ada4d20f28266ec711fb2584a840c07aae50ca1497512c7b9487ed4af7e8ff6e","texture_sha256":"e24fc65a75010833eee2dc6e952bb19e7ba1fd58e89d1b5fe8652603195534f3"}];

const clamp=(v,l,h)=>Math.max(l,Math.min(h,v));
const s=(t,p,phase=0)=>Math.sin(t*Math.PI*2/p+phase);
const blinkCenters=[2.5,6.9,11.8,17.4,22.6,28.9,34.1,40.3,46.8,52.1,57.9,64.3,70.4,75.9,81.6,86.9,93.0,99.5,105.1,111.8,117.3,123.1,129.8,135.3,141.1,147.3,154.8,160.9,167.2,173.8,179.4,185.7,191.5,197.6,204.1,210.6,216.3,223.1,230.2];
const headKeys=[[0,-2,0],[4,6,-1],[9,-8,2],[14,5,-1],[19,-6,3],[24,-9.9,1],[28,8.5,-2],[33,-7,4],[38,6,0],[43,0,0],[51,-5,2],[59,7,-2],[67,-6,3],[75,5,0],[80,-8,2],[85,8,0],[90,-6,1],[100,5,3],[111,-7,0],[121,3,-2],[128,-8,2],[136,8,4],[145,-6,0],[154,7,-2],[162,-8,3],[171,6,0],[180,-5,2],[190,7,-1],[198,-8,3],[205,6,0],[211,-9,4],[216,9.78,-2],[222,-8,2],[227,6,0],[234.066667,-2,0]];
const exprNames=['neutral','happy','sleepy','thinking','surprise'];
const curve=(t)=>{const clock=((t%234.066667)+234.066667)%234.066667;let j=1;while(j<headKeys.length-1&&clock>headKeys[j][0])j++;const a=headKeys[j-1],b=headKeys[j];const u=clamp((clock-a[0])/(b[0]-a[0]),0,1),e=(1-Math.cos(Math.PI*u))/2;return [a[1]+(b[1]-a[1])*e,a[2]+(b[2]-a[2])*e]};
const bodyMotion=c=>({x:1.35*s(c.time,8.5),y:-1.75*(.5+.5*s(c.time,4.8)),r:(.35*s(c.time,6.5)+.12*Math.sin(c.time*.73))*(.9+.2*c.audioEnergy)+c.lookX*.65});
const headMotion=c=>{const [r,nod]=curve(c.time);return {x:-1.25*r+c.lookX*.8,y:nod+c.lookY*1.8,r:r}};
const rearMotion=(c,p)=>{const b=bodyMotion(c),h=headMotion(c),hp=PARTS.find(o=>o.id==='head'),bp=PARTS.find(o=>o.id==='body'),r=b.r*Math.PI/180;return {x:bp.x+b.x+Math.cos(r)*(hp.x+h.x)-Math.sin(r)*(hp.y+h.y),y:bp.y+b.y+Math.sin(r)*(hp.x+h.x)+Math.cos(r)*(hp.y+h.y),r:b.r+h.r}};
const GEOMETRY={"source_canvas":[508,689],"native_height":520,"scale":0.7547169811320755,"anchor":[400,560],"source_anchor":[273.404,650.568],"crop_box":[175.65735849056603,51.005283018867885,595.0535849056604,607.0052830188679]};
const CONTROLS={"mouse":"Head follows mouse gently; no face mesh distortion","EyeBlink / x":"Hold to close eyes","EyeHappy / 1":"Neutral face","EyeJaded / 2":"Happy face","EyeO_O / 3":"Sleepy face","Eye*_* / 4":"Thinking face","Eye@_@ / 5":"Surprise face","expression":"Native expression index 0 neutral, 1 happy, 2 sleepy, 3 thinking, 4 surprise","Wave":"Small hand wave in imported actions","MouthAA / a":"Large open mouth","MouthEE / d":"Medium mouth","MouthOO / w":"Rounded mouth","MouthEH / s":"Small open mouth","MouthOH / e":"Large rounded mouth","mouthOpen":"Recorded vocal-activity opening 0..1; pauses closed","animationTime":"Optional deterministic playback clock in seconds","audioEnergy":"Optional music energy 0..1; subtle amplitude only"};
const MOUTH_GEOMETRY={"head_patch_box":[228,303,275,339],"global_patch_box":[235,310,282,346],"global_mouth_center":[257,325],"shape_bounds_head":{"closed":[233,312,265,325],"small":[242.5,314.0,257.5,322.0],"medium":[239.0,311.5,261.0,324.5],"wide":[236.0,308.5,264.0,327.5],"large":[233.0,305.5,267.0,330.5],"round":[241.0,305.5,259.0,330.5]},"states":["closed","small","medium","wide","large","round"],"thresholds":[0,0.1,0.3,0.5,0.74],"old_mouth_removed_only_for_open_states":true,"method":"Local original-skin patch, narrow baked-stroke mask; code-defined rounded mouth openings","head_source":"head.png","no_face_mesh_warp":true};
const EXPRESSION_GEOMETRY={"global_patch_box":[170,185,352,324],"global_center":[261.0,254.5],"names":["neutral","happy","sleepy","thinking","surprise"],"states_per_expression":["open","closed"],"source_head_sha_preserved":true,"method":"Only baked eye/brow ink cleaned in original local skin patch; code-defined eye/brow poses; rigid native head child","no_face_mesh_warp":true,"original_mouth_untouched":true};
const REPAIR_GEOMETRY={"method":"Original lower-head and body rear-hair pixels moved to one native head-world-following layer behind body; collar removed from rotating head; fixed neck underlap","rear_crop_box":[80,201,445,454],"rear_pivot":[264.626,379.22200000000004],"body_hair_pixels":3286,"head_hair_pixels":5102,"head_face_scale_preserved":true,"source_canvas_unchanged":true,"static_size_unchanged":true};
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
      n.x=c=>p.x+bodyMotion(c).x;
      n.y=c=>p.y+bodyMotion(c).y;
      n.rotation=c=>bodyMotion(c).r;
    } else if(p.id==='head') {
      n.x=c=>p.x+headMotion(c).x;
      n.y=c=>p.y+headMotion(c).y;
      n.rotation=c=>headMotion(c).r;
    } else if(p.id==='rear_hair_follow') {
      n.x=c=>rearMotion(c,p).x;n.y=c=>rearMotion(c,p).y;n.rotation=c=>rearMotion(c,p).r;
    } else if(p.id==='expression_face') {
      n.resource=c=>TEXTURES['expression_'+exprNames[c.expression]+'_'+(c.blink>=.5?'closed':'open')];
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
      n.opacity=0; // The unified native expression_face handles eyelids without duplicate eyes.
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
    defaultKeyMapping:[['EyeBlink','x'],['EyeHappy','1'],['EyeJaded','2'],['EyeO_O','3'],['Eye*_*','4'],['Eye@_@','5'],
      ['MouthAA','a'],['MouthEE','d'],['MouthOO','w'],['MouthEH','s'],['MouthOH','e']],
    metadata:{geometry:GEOMETRY,controls:CONTROLS,resourceCatalog:TEXTURES,mouth:MOUTH_GEOMETRY,expression:EXPRESSION_GEOMETRY,neckHairRepair:REPAIR_GEOMETRY},
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
      if(c.keyInput.includes('Idle'))c.mode=1;
      if(c.keyInput.includes('Sway'))c.mode=2;
      c.expression=liveClock?0:clamp(Math.round(Number(c.expression)||0),0,4);
      ['EyeHappy','EyeJaded','EyeO_O','Eye*_*','Eye@_@'].forEach((key,index)=>{if(c.keyInput.includes(key))c.expression=index});
      if(Number.isFinite(c.expressionOverride))c.expression=clamp(Math.round(c.expressionOverride),0,4);
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
    const fields=['time','lookX','lookY','audioEnergy','blink','wave','mode','mouthOpen','expression'];
    if(fields.every(k=>Number.isFinite(input[k]))&&
      (!Number.isFinite(input.timestamp)||input.timestamp===input._lastTimestamp))return input;
    // One consistent result per raw control object, shared by all components.
    if(normalizedControls.has(input))return normalizedControls.get(input);
    const value=config.parseControl(input);normalizedControls.set(input,value);return value;
  };
  return config;
};
