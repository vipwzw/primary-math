#!/usr/bin/env python3
"""Extract People's Education Press (人教版) subset from the RCAE knowledge graph.

Source: 知识图谱-RCAE/china_primary_school_math_knowledge_graph.json
Output: 知识图谱-RCAE/人教版-小学数学-知识图谱.json

The original file mixes 人教版 + 北师大版 nodes (2264 nodes / 10227 edges).
This script keeps only nodes whose publisher is 人民教育出版社, plus the edges
that connect two such nodes. Useful when feeding NotebookLM, since cross-version
edges cause confusion.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "知识图谱-RCAE" / "china_primary_school_math_knowledge_graph.json"
DST = ROOT / "知识图谱-RCAE" / "人教版-小学数学-知识图谱.json"


def main() -> int:
    if not SRC.exists():
        print(f"ERROR: source file not found: {SRC}", file=sys.stderr)
        print("Did you clone digitalboy/RCAE_graph_data into 知识图谱-RCAE/ ?", file=sys.stderr)
        return 1

    print(f"Loading {SRC.name} ...")
    with SRC.open(encoding="utf-8") as f:
        graph = json.load(f)

    nodes_all = graph.get("nodes", [])
    edges_all = graph.get("edges", [])
    print(f"  source: {len(nodes_all)} nodes, {len(edges_all)} edges")

    keep_nodes = [
        n for n in nodes_all
        if n.get("properties", {}).get("publisher") == "人民教育出版社"
    ]
    keep_uuids = {n["properties"]["uuid"] for n in keep_nodes}

    def edge_endpoints(edge: dict):
        return (
            edge.get("start_uuid") or edge.get("from") or edge.get("source") or edge.get("start"),
            edge.get("end_uuid") or edge.get("to") or edge.get("target") or edge.get("end"),
        )

    keep_edges = []
    for e in edges_all:
        a, b = edge_endpoints(e)
        if a in keep_uuids and b in keep_uuids:
            keep_edges.append(e)

    out = {"nodes": keep_nodes, "edges": keep_edges}
    print(f"  kept (PEP only): {len(keep_nodes)} nodes, {len(keep_edges)} edges")

    DST.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    size_mb = DST.stat().st_size / 1048576
    print(f"Wrote {DST}  ({size_mb:.2f} MB)")

    grades: dict[str, int] = {}
    for n in keep_nodes:
        g = n["properties"].get("grade", "未知")
        grades[g] = grades.get(g, 0) + 1
    print("Per-grade node counts:")
    for g in sorted(grades):
        print(f"  {g}: {grades[g]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
