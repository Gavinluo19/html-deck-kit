# 07 · 线性图标（18 个，可直接复制）

规则：图标只用线性 SVG（规范 V3）。`class="ic"` 会让图标跟随文字颜色、大小约等于字号；需要圆形底时外面包 `<span class="icb">`。

```html
<svg class="ic" viewBox="0 0 24 24">…路径…</svg>
<span class="icb"><svg class="ic" viewBox="0 0 24 24">…</svg></span>
```

以下图标为本项目自绘，随 MIT 许可使用。

| 名称 | 适合表达 | 代码 |
|---|---|---|
| `user` | 人 / 用户 | `<svg class="ic" viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-6 8-6s8 2 8 6"/></svg>` |
| `users` | 团队 / 人群 | `<svg class="ic" viewBox="0 0 24 24"><circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c0-3.5 3-5.5 6.5-5.5s6.5 2 6.5 5.5"/><path d="M16 4.6a3.5 3.5 0 0 1 0 6.8"/><path d="M18 14.8c2.2.6 3.5 2.4 3.5 5.2"/></svg>` |
| `target` | 目标 / 场景 | `<svg class="ic" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5"/></svg>` |
| `search` | 找问题 / 调研 | `<svg class="ic" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg>` |
| `layers` | 拆解 / 分层 | `<svg class="ic" viewBox="0 0 24 24"><path d="M12 3l9 5-9 5-9-5z"/><path d="M3 13l9 5 9-5"/></svg>` |
| `database` | 数据 | `<svg class="ic" viewBox="0 0 24 24"><ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5"/><path d="M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/></svg>` |
| `book` | 知识 / 方法 | `<svg class="ic" viewBox="0 0 24 24"><path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path d="M19 19v2H6"/></svg>` |
| `bulb` | 想法 / 洞察 | `<svg class="ic" viewBox="0 0 24 24"><path d="M9 18h6"/><path d="M10 21h4"/><path d="M12 3a6 6 0 0 0-4 10.5c.8.8 1 1.5 1 2.5h6c0-1 .2-1.7 1-2.5A6 6 0 0 0 12 3z"/></svg>` |
| `chart` | 结果 / 数据图 | `<svg class="ic" viewBox="0 0 24 24"><path d="M4 20V10"/><path d="M10 20V4"/><path d="M16 20v-7"/><path d="M3 20h18"/></svg>` |
| `chat` | 用户原话 / 访谈 | `<svg class="ic" viewBox="0 0 24 24"><path d="M4 5h16v11H9l-5 4z"/></svg>` |
| `check` | 完成 / 达标 | `<svg class="ic" viewBox="0 0 24 24"><path d="M5 12l5 5 9-10"/></svg>` |
| `alert` | 风险 / 卡点 | `<svg class="ic" viewBox="0 0 24 24"><path d="M12 3l10 18H2z"/><path d="M12 10v5"/><path d="M12 18h.01"/></svg>` |
| `clock` | 时间 / 效率 | `<svg class="ic" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>` |
| `link` | 连接 / 对应关系 | `<svg class="ic" viewBox="0 0 24 24"><path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/></svg>` |
| `flag` | 里程碑 / 行动 | `<svg class="ic" viewBox="0 0 24 24"><path d="M5 21V4"/><path d="M5 4h11l-2 4 2 4H5"/></svg>` |
| `arrow` | 下一步 | `<svg class="ic" viewBox="0 0 24 24"><path d="M5 12h14"/><path d="M13 6l6 6-6 6"/></svg>` |
| `loop` | 迭代 / 循环 | `<svg class="ic" viewBox="0 0 24 24"><path d="M20 12a8 8 0 0 1-14 5.3"/><path d="M4 12a8 8 0 0 1 14-5.3"/><path d="M18 3v4h-4"/><path d="M6 21v-4h4"/></svg>` |
| `tool` | 工具 | `<svg class="ic" viewBox="0 0 24 24"><path d="M14.5 5.5a4 4 0 0 0-5 5L4 16v4h4l5.5-5.5a4 4 0 0 0 5-5l-2.5 2.5-2.5-.5-.5-2.5z"/></svg>` |

需要更多图标时：只用同一风格（24×24、2px 描边、圆角端点）的开源线性图标，并保留其许可证说明。
