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
完成后运行 python3 html-deck-kit/tools/check_layout.py <文件>，错误为 0。
```

## 3. WorkBuddy、飞书（智能体 / 多维表格 AI）等办公类 Agent

上传 **`SPEC-ALL.md`（规范全集，一个文件）+ `template/deck-template.html`** 两个文件作为知识（v2.2 起；规范更新后运行 `python3 tools/build_spec_all.py` 重新生成），提示词：

```
你是 HTML 演讲稿制作助手。严格遵守上传的《01-spec 严格规范》。
输出必须是基于 deck-template.html 的完整单文件 HTML，只增删 <section class="slide">。
保留母版左下角署名 #tplcredit（Template by Gavin © 2026），不得删除或改字。
每页：eyebrow + h2 + （用到模型时）mdl 模型标签 + body + kick + foot + aside.notes。
每页声明版面档位：标准页 y ≤ 630px（默认）；图解页 data-zone="75" y ≤ 675px；全幅页 data-zone="full" y ≤ 830px（≤ 全稿 20%，结论写进标题）。
标题写结论，≤ 20 字；讲者提示只写进讲稿；自绘 SVG 只用 var(--token)。
动效每页最多 1 种（M1–M6），先说清它说明什么关系，否则不加。
```

## 4. 修改闭环（v2.0）

把 HTML 里按 E 写好的“修改汇总”复制出来，连同 HTML 交给 AI：

```
这是演讲稿的修改汇总（格式：【第 N 页 · 页面id】标题 + 意见）。
请按 html-deck-kit 规范逐页修改：只改列出的页，页面 id 不变；
改完运行 python3 tools/check_layout.py 文件.html 和 --zoom 1.3，确保错误为 0。
```

用筛片台“复制清单”挑页时：

```
按这份放映清单，生成一个只包含这些页、按此顺序排列的新 HTML，其余页删除，页面 id 不变。
```

## 4b. 加动效（v2.2）

```
按 html-deck-kit 01-spec §5b 给这份演讲稿加动效。逐页判断：
这一页要说明的是顺序 / 焦点 / 重点 / 数量 / 前后接续 / 替换中的哪一种？
说不出就不加。每页最多 1 种（M1–M6），写法照 04-interaction §2d。
改完运行 check_layout.py，警告里不能出现“动效 >1 种”。
```

## 5. 常用指令

| 想要 | 这样说 |
|---|---|
| 换默认主题 | “把默认主题改成 stellar（`<html data-theme="stellar">`）” |
| 加一套自己的主题 | “按 03-themes 第 4 节新增主题 `brand-x`，主色 #xxxxxx” |
| 页面太满 | “第 N 页超出底线，按 L5 规则处理：先拆页，再考虑升为图解页或全幅页” |
| 加动效 | “第 N 页要说明的是顺序关系，用 M1 连线画出；其他页不加” |
| 画关系图 | “把这段流程画成 T20 泳道图（全幅页），跨部门交接用强调色并计数” |
| 对外版 | “这份要对外讲：去掉客户真名，截图打码，交付前按 K 检查一遍” |
| 只要精讲 | “只做 data-tier=c 的页面，完整版页面先列在大纲里” |
| 加模型卡 | “给第 N 页的模型加一张模型卡（T8），默认隐藏，加 mchip 入口” |
