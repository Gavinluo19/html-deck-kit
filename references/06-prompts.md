# 06 · 在不同 AI 工具里怎么用

核心做法都一样：**把整个 `html-deck-kit` 文件夹交给 AI，让它先读 `SKILL.md` 和 `references/01-spec.md`，再动手。**

## 1. Claude（Claude.ai / Claude Code / Cowork）

- 作为 Skill 安装：把 `html-deck-kit` 文件夹放进 Skills 目录（或在 Claude.ai 上传为技能）。之后直接说“用 deck-kit 把这份讲稿做成 HTML 演讲稿”。
- 不安装也可以：把文件夹上传或连接到会话，第一句话写：

```
请先阅读 html-deck-kit/SKILL.md 和 references/01-spec.md，严格按规范，
以 template/deck-template.html 为母版，把附件讲稿做成 HTML 演讲稿。
默认主题 warm，精讲 45 页左右。先给我逐页大纲，我确认后再做页面。
```

## 2. Codex / Cursor / Trae 等代码类 Agent

把文件夹放进项目根目录，在 `AGENTS.md`（或项目规则）中加一行：

```
制作 HTML 演讲稿时，必须遵守 ./html-deck-kit/SKILL.md 与 ./html-deck-kit/references/*.md；
完成后运行 python3 html-deck-kit/tools/check_layout.py <文件> 且无 OVER。
```

## 3. WorkBuddy、飞书（智能体 / 多维表格 AI）等办公类 Agent

上传 `SKILL.md`、`references/01-spec.md`、`references/02-components.md`、`template/deck-template.html` 四个文件作为知识，提示词：

```
你是 HTML 演讲稿制作助手。严格遵守上传的《01-spec 严格规范》。
输出必须是基于 deck-template.html 的完整单文件 HTML，只增删 <section class="slide">。
每页：eyebrow + h2 + （用到模型时）mdl 模型标签 + body + kick + foot + aside.notes。
正文与结论行不得超过画面上方 70%（y ≤ 630px）。
```

## 4. 常用指令

| 想要 | 这样说 |
|---|---|
| 换默认主题 | “把默认主题改成 stellar（`<html data-theme="stellar">`）” |
| 加一套自己的主题 | “按 03-themes 第 4 节新增主题 `brand-x`，主色 #xxxxxx” |
| 页面太满 | “第 N 页超出 70% 线，按 L5 规则处理：先拆页” |
| 只要精讲 | “只做 data-tier=c 的页面，完整版页面先列在大纲里” |
| 加模型卡 | “给第 N 页的模型加一张模型卡（T8），默认隐藏，加 mchip 入口” |
