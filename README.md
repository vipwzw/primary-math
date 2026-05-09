# 小学数学学习资料库

本仓库收集和整理小学数学学习相关的开源资料，目标是支持基于 AI 的"48 小时压缩学习法"。

## 当前内容

### 1. 人教版小学数学电子课本（1–6 年级，全 12 册）

- 目录：`小学数学-人教版/`（**PDF 已入库**，约 294 MB，最大单文件 48 MB）
- 下载脚本：`scripts/download_pep_math.sh`（用于重新生成或校验）
- 数据来源：[TapXWorld/ChinaTextbook](https://github.com/TapXWorld/ChinaTextbook)
- 详情见 [`小学数学-人教版/README.md`](./小学数学-人教版/README.md)

直接 `git clone` 即可拿到所有 PDF。如需重新下载：

```bash
bash scripts/download_pep_math.sh
```

### 2. 小学数学知识图谱（RCAE 数据集 + 人教版子集）

- 目录：`知识图谱-RCAE/`
- 提取脚本：`scripts/extract_pep_math_graph.py`
- 数据来源：[digitalboy/RCAE_graph_data](https://github.com/digitalboy/RCAE_graph_data)（CC BY-NC 4.0）
- 详情见 [`知识图谱-RCAE/README.local.md`](./知识图谱-RCAE/README.local.md)

包含原始全量图（2264 节点 / 10227 边）+ **人教版子集**（1632 节点 / 7726 边）。
重新生成人教版子集：

```bash
python3 scripts/extract_pep_math_graph.py
```

### 依赖

`bash`, `curl`, `jq`, `python3`, `awk`
