#!/usr/bin/env python3
"""Package the importable model plus deterministic actions and build inputs."""
import argparse, hashlib, json, zipfile
from pathlib import Path

BASE=Path(__file__).resolve().parent
MODEL_NAME='GUMI_大脸Q版_小初音工作室随唱口型模型.js'

def sha(data):return hashlib.sha256(data).hexdigest()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True,type=Path)
    args=ap.parse_args();args.output.parent.mkdir(parents=True,exist_ok=True)
    manifest=json.loads((BASE/'model_manifest.json').read_text())
    for key in ('native_js','sample_file','control_manifest','actions','sampler','assets_manifest','mouth_envelope'):
        binding=manifest[key]
        assert sha((BASE/binding['path']).read_bytes())==binding['sha256'],key
    files={}
    for p in BASE.rglob('*'):
        if p.is_file() and not any(x in p.parts for x in ('__pycache__','node_modules','.cache')):
            files['model/'+str(p.relative_to(BASE))]=p
    files[MODEL_NAME]=BASE/'native-model.js'
    files['audio_features.npz']=BASE.parent/'audio_features.npz'
    rigdir=BASE.parent/'assets/gumi'
    files['assets/gumi/rig_exports.json']=rigdir/'rig_exports.json'
    for p in (rigdir/'parts').glob('*.png'):files['assets/gumi/parts/'+p.name]=p
    readme='''GUMI 大脸 Q 版 · 小初音工作室 Reborn 模型包

直接导入：Settings（设置）页 → 文件夹图标“导入模型” → 根目录的 GUMI_大脸Q版_小初音工作室随唱口型模型.js。
全部图片已嵌入 JS，不需要选择 PNG。背景页可选择 Paper 或透明。
X 闭眼，1 安静待机，2 轻摆，鼠标轻移让角色歪头。
A/D/W/S/E 分别是大开口、中开口、圆口、小开口、大圆口；松开按键恢复闭口。

录制回放：Timeline（时间轴）页 → 导入动作 → model/HMSR_GUMI_PV.json。
动作约 234 秒、60 fps，与最终 PV 使用相同的角色模型和控制曲线。
新嘴部跟随演唱活动开合，长停顿与间奏闭口；属于人声活动近似，非逐音素对齐。
音乐、歌词排版、景物动画与可视化请使用完整 PV 制作工程；本模型包不包含音乐。

详细说明：model/模型使用说明.txt。
模型采样只需 Node 18+，无需 npm 安装：
  node model/sample_native_model.mjs
可在本包内重新从拆层素材导出（需要 Python、Pillow、NumPy、OpenCV）：
  python model/build_model.py
  node model/sample_native_model.mjs
重采样会更新 model/ 内的样本、资源与 SHA 清单。

本包包含真实上游 importer / physics runtime，原始来源和源码 SHA 见
model/upstream_runtime/UPSTREAM_NOTICE.txt 与 upstream_source_manifest.json。
'''
    data_manifest={'schema':'gumi-halfne-model-bundle-v1','files':{
      name:{'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size} for name,p in sorted(files.items())}}
    with zipfile.ZipFile(args.output,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for name,p in sorted(files.items()):z.write(p,name)
        z.writestr('README.txt',readme)
        z.writestr('bundle_manifest.json',json.dumps(data_manifest,ensure_ascii=False,indent=2))
    with zipfile.ZipFile(args.output) as z:
        assert z.testzip() is None
        for name,record in data_manifest['files'].items():assert sha(z.read(name))==record['sha256']
        assert z.read(MODEL_NAME)==(BASE/'native-model.js').read_bytes()
    report={'passed':True,'zip':str(args.output.resolve()),'bytes':args.output.stat().st_size,
      'sha256':sha(args.output.read_bytes()),'files':len(files)+2,
      'native_js_sha256':manifest['native_js']['sha256'],'crc_and_member_sha256':True}
    print(json.dumps(report,ensure_ascii=False))

if __name__=='__main__':main()
