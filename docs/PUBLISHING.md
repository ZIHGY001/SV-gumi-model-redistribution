# 发布到 GitHub

建议仓库名：`gumi-chibi-hmsr`。

仓库简介：`A soft pencil-style chibi GUMI model for Halfne Miku Studio Reborn, with five expressions and native mouth controls.`

建议 Topics：`gumi`、`halfne-miku-studio`、`chibi`、`character-model`。

1. 解压 `gumi-chibi-hmsr-v1.0.0-github-source.zip`。
2. 将 `gumi-chibi-hmsr` 文件夹内的文件上传到仓库根目录，保留目录结构。
3. 创建 Release，标签填写 `v1.0.0`，标题填写 `v1.0.0 · GUMI Q 版模型`。
4. 将 RELEASE_NOTES.md 的正文用作发行说明，并附上 `gumi-chibi-hmsr-v1.0.0-model-release.zip`。
5. README 中的预览使用相对路径，上传后会自动显示。保留 CREDITS.md 和 LICENSE_NOTICE.md 的来源及许可范围说明。

如需用 Git 命令上传，初始化及提交可以在本地完成；`<你的仓库地址>` 需替换为自己的实际 GitHub 仓库地址：

```sh
git init
git add .
git commit -m "Release GUMI chibi model v1.0.0"
git branch -M main
git remote add origin <你的仓库地址>
git push -u origin main
git tag v1.0.0
git push origin v1.0.0
```

这份发行包已准备好文件内容，但没有替你在 GitHub 上创建仓库或发布 Release。
