#!/usr/bin/env python3
"""
HTML Deck Kit · 版面检查（70% 规则）

用法：
  pip install playwright && python -m playwright install chromium
  python3 tools/check_layout.py my-deck.html            # 默认字号（112%）检查
  python3 tools/check_layout.py my-deck.html --zoom 1.3 # 最大字号检查（受 data-czmax 限制）
  python3 tools/check_layout.py my-deck.html --shots out/ --theme stellar   # 顺便逐页截图

输出：每页内容最低点的 y 坐标；超过 630px 标记 OVER。
"""
import argparse, asyncio, os, sys
from playwright.async_api import async_playwright

LIMIT = 630
SKIP = ("hero",)  # 封面 / 结尾不检查


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
        await pg.add_style_tag(content="#hint,.fbtn,#segbar,#progress{display:none!important}")
        n = await pg.evaluate("document.querySelectorAll('.slide').length")
        over = 0
        for i in range(n):
            info = await pg.evaluate(f"""(() => {{
              const s = document.querySelectorAll('.slide')[{i}];
              window.__jump({i + 1});
              s.querySelectorAll('.step').forEach(e => e.classList.add('on'));
              const cap = parseFloat(s.dataset.czmax || '9');
              s.style.setProperty('--cz', Math.min({a.zoom}, cap));
              return [s.id, s.className, s.querySelectorAll('.step').length,
                      s.querySelectorAll('aside.notes p[data-s]').length];
            }})()""")
            await pg.wait_for_timeout(450)
            sid, cls, steps, notes = info
            if any(k in cls.split() for k in SKIP):
                print(f"{i+1:>3} {sid:<18} (封面/结尾，跳过)")
            else:
                y = await pg.evaluate(f"""(() => {{
                  const s = document.querySelectorAll('.slide')[{i}], t = s.getBoundingClientRect().top; let m = 0;
                  s.querySelectorAll('*').forEach(e => {{
                    if (e.closest('.foot,aside,.hidbadge') || e.matches('.pageno')) return;
                    const q = e.getBoundingClientRect(); if (q.height < 1) return; m = Math.max(m, q.bottom - t);
                  }}); return Math.round(m); }})()""")
                flag = "OVER" if y > LIMIT else "ok"
                if y > LIMIT:
                    over += 1
                note_flag = "" if notes == steps + 1 else f"  讲稿段数 {notes} ≠ 步数+1 ({steps + 1})"
                print(f"{i+1:>3} {sid:<18} y={y:<4} {flag}{note_flag}")
            if a.shots:
                os.makedirs(a.shots, exist_ok=True)
                await pg.screenshot(path=os.path.join(a.shots, f"{i+1:02d}_{sid}.png"))
        print(f"\n共 {n} 页；超出 70% 线：{over} 页；脚本错误：{errors or '无'}")
        await b.close()
        sys.exit(1 if over else 0)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--zoom", type=float, default=1.12)
    ap.add_argument("--theme", default=None)
    ap.add_argument("--shots", default=None)
    asyncio.run(main(ap.parse_args()))
