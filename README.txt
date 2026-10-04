GUMI 大脸 Q 版 · 小初音工作室 Reborn 模型包

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
