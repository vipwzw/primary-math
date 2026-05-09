# 小学数学学习资料库

本仓库收集和整理小学数学学习相关的开源资料，目标是支持基于 AI 的"48 小时压缩学习法"。

## 当前内容

### 1. 人教版小学数学电子课本（1–6 年级，全 12 册）

- 目录：`小学数学-人教版/`
- 下载脚本：`scripts/download_pep_math.sh`
- 数据来源：[TapXWorld/ChinaTextbook](https://github.com/TapXWorld/ChinaTextbook)
- 详情见 [`小学数学-人教版/README.md`](./小学数学-人教版/README.md)

PDF 文件本身不入库（约 294 MB，已在 `.gitignore` 中排除）。
首次使用请运行：

```bash
bash scripts/download_pep_math.sh
```

依赖：`bash`, `curl`, `jq`, `python3`, `awk`。
