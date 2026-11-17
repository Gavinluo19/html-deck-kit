#!/usr/bin/env python3
"""
HTML Deck Kit · 版面检查（v2.2：版面三档 + 内容规则）

用法：
  pip install playwright && python -m playwright install chromium
  python3 tools/check_layout.py my-deck.html                 # 默认字号 112%
  python3 tools/check_layout.py my-deck.html --zoom 1.3      # 最大字号（引擎按页自动适配）
  python3 tools/check_layout.py my-deck.html --theme notebook --shots out/
  python3 tools/check_layout.py my-deck.html --motion        # 逐步播放，核对动效终态

错误（退出码 1）：内容超过本页档位底线、右侧越界、画面禁入词、id 缺失或重复、缺少署名。
警告（不影响退出码）：讲稿段数、标题字数与行数、字号过小、截字、每页动效超过 1 种、金句页与全幅页占比。

版面档位（data-zone）：默认 630px（70%）· "75" 675px · "full" 830px；章节页 780px；封面 / 结尾不检查。
"""
import argparse, asyncio, os, sys
from playwright.async_api import async_playwright

BANNED = ["问全场", "这里停一下", "停一下", "挑几条讲", "教学示例", "以下为假设", "本节交付", "课堂提问：", "现场练习："]

MEASURE = r"""(arg) => {
  const [i, banned] = arg;
  const s = document.querySelectorAll('.slide')[i];
  const r0 = s.getBoundingClientRect(), k = r0.width / 1600;
  const hero = s.classList.contains('hero'), act = s.classList.contains('act');
  const lim = hero ? 0 : act ? 780 : (window.__zoneLim ? window.__zoneLim(s) : 630);
  const skipEl = e => e.closest('.foot,aside,.hidbadge,#tplcredit') || e.matches('.pageno');
  let bot = 0, right = 0, rightEl = '';
  s.querySelectorAll('*').forEach(e => {
    if (skipEl(e) || e.matches('canvas,.veil,.grain')) return;
    const q = e.getBoundingClientRect(); if (q.height < 1 || q.width < 1) return;
    const cs = getComputedStyle(e); if (cs.visibility === 'hidden' || cs.display === 'none') return;
    bot = Math.max(bot, (q.bottom - r0.top) / k);
    const rr = (q.right - r0.left) / k; if (rr > right) { right = rr; rightEl = e.tagName.toLowerCase() + (e.className && typeof e.className === 'string' ? '.' + e.className.split(' ')[0] : ''); }
  });
  const zoomOf = e => { let z = 1; for (let a = e; a && a !== document.documentElement; a = a.parentElement) { const v = parseFloat(getComputedStyle(a).zoom || '1'); if (v) z *= v; } return z; };
  const small = [], clip = [];
  s.querySelectorAll('*').forEach(e => {
    if (skipEl(e) || e.closest('#tplcredit,.credit')) return;
    const own = [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
    if (!own) return;
    const q = e.getBoundingClientRect(); if (q.height < 1) return;
    let fs;
    if (e.closest('svg')) { const svg = e.closest('svg'), vb = svg.viewBox && svg.viewBox.baseVal; const sc = vb && vb.width ? svg.getBoundingClientRect().width / k / vb.width : 1; fs = parseFloat(getComputedStyle(e).fontSize) * sc; }
    else fs = parseFloat(getComputedStyle(e).fontSize) * zoomOf(e);
    if (fs < (e.closest('svg') ? 13.95 : 12.95)) small.push(Math.round(fs * 10) / 10 + 'px「' + e.textContent.trim().slice(0, 8) + '」');
    if (!e.closest('svg') && e.scrollWidth > e.clientWidth + 2 && /hidden|clip/.test(getComputedStyle(e).overflowX)) clip.push(e.textContent.trim().slice(0, 10));
  });
  const h2 = s.querySelector('h2');
  let tlen = 0, tlines = 0;
  if (h2) { tlen = h2.textContent.replace(/\s/g, '').length; const lh = parseFloat(getComputedStyle(h2).lineHeight) || 56; tlines = Math.round(h2.getBoundingClientRect().height / k / (lh * zoomOf(h2))); }
  const vis = [...s.querySelectorAll('*')].filter(e => !e.closest('aside,.foot')).map(e => [...e.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent).join('')).join(' ');
  const bad = banned.filter(w => vis.includes(w));
  const mx = [];
  if (s.querySelector('.mx-draw')) mx.push('M1 画线');
  if (s.querySelector('[data-mx~="focus"]')) mx.push('M2 聚光');
  if (s.querySelector('.mx-sweep,.mx-ring,.mx-under,.mx-strike')) mx.push('M3 标注');
  if (s.querySelector('[data-count]')) mx.push('M4 数字');
  if (s.querySelector('[data-out]')) mx.push('M6 替换');
  const groups = window.__deck && window.__deck.steps ? window.__deck.steps(s).length : s.querySelectorAll('.step').length;
  return { id: s.id, cls: s.className, zone: s.dataset.zone || '', lim, bot: Math.round(bot), right: Math.round(right), rightEl,
           small: small.slice(0, 3), clip: clip.slice(0, 3), tlen, tlines, bad, mx,
           steps: groups, notes: s.querySelectorAll('aside.notes p[data-s]').length, stmt: s.classList.contains('stmt'), hid: s.dataset.hidden === '1' || s.dataset.tier === 'x' };
}"""


async def main(a):
    path = os.path.abspath(a.file)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1600, "height": 900})
        errors = []
        pg.on("pageerror", lambda e: errors.append(str(e)))
        await pg.goto("file://" + path)
        await pg.wait_for_timeout(1200)
        if a.theme:
            await pg.evaluate(f"window.__setTheme && window.__setTheme('{a.theme}')")
            await pg.wait_for_timeout(300)
        await pg.add_style_tag(content="#hint,.fbtn,#segbar,#progress{display:none!important}")
        lv = await pg.evaluate("window.__fzLevels || [1,1.06,1.12,1.18,1.24,1.3]")
        idx = min(range(len(lv)), key=lambda j: abs(lv[j] - a.zoom))
        await pg.evaluate(f"window.__setFz && window.__setFz({idx})")
        if not a.motion:
            await pg.evaluate("document.body.classList.add('nomx')")
        n = await pg.evaluate("document.querySelectorAll('.slide').length")
        err = warn = 0
        stmt = full = shown = 0
        for i in range(n):
            if a.motion:
                await pg.evaluate(f"window.__jump({i + 1})")
                steps = await pg.evaluate(f"window.__deck.steps(document.querySelectorAll('.slide')[{i}]).length")
                for _ in range(steps):
                    await pg.keyboard.press("ArrowRight")
                    await pg.wait_for_timeout(1000)
                await pg.wait_for_timeout(600)
            else:
                await pg.evaluate(f"""(() => {{
                  window.__jump({i + 1});
                  const s = document.querySelectorAll('.slide')[{i}];
                  s.querySelectorAll('.step').forEach(e => e.classList.add('on'));
                  s.querySelectorAll('[data-out]:not(.step)').forEach(e => e.classList.add('gone'));
                  window.__balance && window.__balance();
                }})()""")
                await pg.wait_for_timeout(350)
            r = await pg.evaluate(MEASURE, [i, BANNED])
            if not r["hid"]:
                shown += 1; stmt += r["stmt"]; full += r["zone"] == "full"
            msgs, bad = [], False
            if r["lim"]:
                if r["bot"] > r["lim"]:
                    msgs.append(f"OVER 底线 {r['lim']}"); bad = True
            if r["lim"] and r["right"] > 1560:
                msgs.append(f"右侧越界 x={r['right']}（{r['rightEl']}）"); bad = True
            if r["bad"]:
                msgs.append("画面禁入词：" + "、".join(r["bad"])); bad = True
            w = []
            if r["notes"] != r["steps"] + 1:
                w.append(f"讲稿段数 {r['notes']} ≠ 步数+1（{r['steps'] + 1}）")
            if r["tlen"] > 20 and not r["stmt"]:
                w.append(f"标题 {r['tlen']} 字 > 20")
            if r["tlines"] > 2:
                w.append(f"标题 {r['tlines']} 行")
            if r["small"] and lv[idx] >= 1.12:
                w.append("字号过小 " + " ".join(r["small"]))
            if r["clip"]:
                w.append("截字 " + " / ".join(r["clip"]))
            if len(r["mx"]) > 1:
                w.append("动效 >1 种：" + "、".join(r["mx"]))
            err += bad; warn += bool(w)
            zone = {"": "70%", "75": "75%", "full": "全幅"}.get(r["zone"], r["zone"])
            if not r["lim"]:
                head = f"{i+1:>3} {r['id']:<14} (封面/结尾)"
            else:
                head = f"{i+1:>3} {r['id']:<14} {zone:<4} y={r['bot']:<4}/{r['lim']}"
            print(head, ("ERROR " + "；".join(msgs)) if msgs else "ok", ("  ⚠ " + "；".join(w)) if w else "")
            if a.shots:
                os.makedirs(a.shots, exist_ok=True)
                await pg.screenshot(path=os.path.join(a.shots, f"{i+1:02d}_{r['id']}.png"))
        dup = await pg.evaluate("(()=>{const ids=[...document.querySelectorAll('.slide')].map(s=>s.id);return ids.filter((x,i)=>!x||ids.indexOf(x)!==i)})()")
        if dup:
            print("ERROR 页面 id 缺失或重复（筛片台与修改意见按 id 保存）：", dup); err += 1
        if not await pg.evaluate("!!document.querySelector('#tplcredit')"):
            print("ERROR 缺少左下角署名 #tplcredit（规则 F7）"); err += 1
        if shown and stmt / shown > 0.08:
            print(f"⚠ 金句页 {stmt}/{shown} 页，超过 8%（V9）"); warn += 1
        if shown and full / shown > 0.20:
            print(f"⚠ 全幅页 {full}/{shown} 页，超过 20%（L3）"); warn += 1
        if errors:
            err += 1
        print(f"\n共 {n} 页；错误 {err}；警告 {warn}；字号 {lv[idx]:.2f}；脚本错误：{errors or '无'}")
        await b.close()
        sys.exit(1 if err else 0)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--zoom", type=float, default=1.12)
    ap.add_argument("--theme", default=None)
    ap.add_argument("--shots", default=None)
    ap.add_argument("--motion", action="store_true")
    asyncio.run(main(ap.parse_args()))
