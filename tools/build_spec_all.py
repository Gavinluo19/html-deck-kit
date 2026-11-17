#!/usr/bin/env python3
"""把 SKILL.md 与 references/*.md 合成一个 SPEC-ALL.md，方便上传到只接受少量文件的 Agent（飞书、WorkBuddy 等）。

用法：python3 tools/build_spec_all.py        # 在仓库根目录生成 SPEC-ALL.md
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARTS = ["SKILL.md", "references/01-spec.md", "references/02-components.md", "references/03-themes.md",
         "references/04-interaction.md", "references/05-checklist.md", "references/07-icons.md"]

def main():
    out = ["# HTML Deck Kit · 规范全集（自动合成，请勿手改）\n",
           "> 本文件由 `tools/build_spec_all.py` 从 SKILL.md 与 references/ 合成。",
           "> 交给 Agent 时：本文件 + `template/deck-template.html` 两个文件即可开工；需要检查时再加 `tools/check_layout.py`。\n"]
    for p in PARTS:
        t = open(os.path.join(ROOT, p), encoding="utf-8").read()
        t = re.sub(r"\A---\n.*?\n---\n", "", t, flags=re.S)  # 去掉 SKILL.md 的 frontmatter
        t = re.sub(r"^(#{1,5}) ", lambda m: "#" + m.group(1) + " ", t, flags=re.M)  # 标题整体降一级
        out.append(f"\n---\n\n<!-- 来源：{p} -->\n")
        out.append(t.strip() + "\n")
    open(os.path.join(ROOT, "SPEC-ALL.md"), "w", encoding="utf-8").write("\n".join(out))
    print("SPEC-ALL.md written")

if __name__ == "__main__":
    main()
