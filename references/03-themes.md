# 03 · 主题（配色与视觉）

六套主题共用同一组 token。切换方式：`<html data-theme="warm">`，或演示时按 **T**，或在网址后加 `?theme=stellar`。

> 主题中不含任何品牌标志或专有字体。

## 1. 主题一览

| id | 名称 | 气质 | 背景 / 文字 | 主强调 `--clay` | 次强调 `--kraft` / `--sky` | 标题字体 | 封面 |
|---|---|---|---|---|---|---|---|
| `warm`（默认） | 暖纸 Warm Paper | 温暖、学术、像纸质讲义 | `#F5F3EC` / `#1F1E1B` | `#C9623F` 陶土橙 | `#C99A72` / `#4F86B8` | 宋体衬线 | 深色 + 暖色网络动画 |
| `mono` | 极简黑白 Mono | 克制、留白、工程感 | `#FFFFFF` / `#0D0D0D` | `#10A37F` 青绿 | `#6E6E80` / `#2563EB` | 无衬线 | 纯黑 |
| `void` | 深空 Void | 全深色、科技、对比强 | `#000000` / `#E7E9EA` | `#1D9BF0` 亮蓝 | `#8B98A5` / `#A78BFA` | 无衬线 | 纯黑 |
| `lunar` | 月光 Lunar | 清爽、理性、蓝白 | `#F7F8FA` / `#0B0D12` | `#1783FF` 月光蓝 | `#5B6B86` / `#12B886` | 无衬线 | 深夜蓝 |
| `linen` | 素白 Plain Linen | 安静、编辑感、浅色封面 | `#F8F8F7` / `#1A1A19` | `#34507A` 墨蓝 | `#A39E93` / `#5F7F5F` | 宋体衬线 | **浅色** |
| `stellar` | 星光渐变 Stellar | 明亮、渐变、产品发布会 | `#FFFFFF` / `#1F1F1F` | `#1A73E8` 蓝 | `#9B72CB` / `#D96570` | 无衬线 | 深灰 + 蓝紫粉渐变 |

## 2. Token 表（每个主题都必须完整定义）

| Token | 作用 |
|---|---|
| `--paper` / `--paper-2` | 页面底色 / 次级底色（表头、标签底） |
| `--card` / `--line` | 卡片底色 / 分隔线与描边 |
| `--ink` / `--ink-2` / `--ink-3` | 主文字 / 次文字 / 弱文字 |
| `--clay` / `--clay-soft` | 主强调色 / 主强调浅底 |
| `--kraft` / `--manilla` | 次强调色 / 次强调浅底 |
| `--sky` / `--sky-soft` | 信息色（模型、AI） / 浅底 |
| `--warn` | 风险、负面 |
| `--slate` / `--on-slate` / `--on-slate-2` | 深色章节页底色 / 文字 / 弱文字 |
| `--f-display` / `--f-body` / `--f-mono` | 标题字体 / 正文字体 / 数字字体 |
| `--hero-bg` / `--hero-ink` / `--hero-sub` / `--hero-org` / `--hero-lb` / `--hero-credit` | 封面底色与各级文字 |
| `--hero-grad` / `--hero-veil` / `--hero-grain` | 封面标题渐变 / 遮罩 / 网格线 |
| `--net-1` `--net-2` `--net-3` `--net-pulse` | 封面网络动画颜色（写成 `r,g,b`） |
| `--hl-line` / `--blue-line` / `--frame-bg` | 强调框描边 / 信息框描边 / 图框底色 |
| `--stage-bg` | 画布外的舞台底色 |

## 3. 字体栈（必须带本地后备）

```css
--f-display: "Noto Serif SC","Noto Serif CJK SC","Songti SC","STSong",serif;          /* 衬线主题 */
--f-display: "Inter","Noto Sans SC","Noto Sans CJK SC","PingFang SC",system-ui,sans-serif; /* 无衬线主题 */
--f-body:    "Noto Sans SC","Noto Sans CJK SC","PingFang SC","Microsoft YaHei",system-ui,sans-serif;
```

## 4. 新增主题的规则

1. 复制 `themes/themes.css` 中任一主题块，改选择器为 `[data-theme="你的id"]`，**所有 token 都要填**。
2. 对比度：正文与底色 ≥ 4.5:1；44px 以上大字 ≥ 3:1。
3. `--clay`、`--kraft`、`--sky` 三个强调色要能靠**明度**区分，不只靠色相。
4. 在模板脚本的 `TH` 数组与 `TN` 名称表中加上新主题，按 T 能切到。
5. 用 `tools/check_layout.py` 截图检查 6 类页面：封面、总分总、概念页、案例卡、四象限、章节页。
