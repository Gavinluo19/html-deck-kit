#!/usr/bin/env python3
"""
HTML Deck Kit · 字体内嵌（可选）

把演讲稿里实际用到的字，从你电脑上的字体文件里抽出来（子集化），
以 base64 内嵌进 HTML。换电脑、断网、投影机电脑没有思源字体，显示也一致。

用法：
  pip install fonttools brotli
  python3 tools/embed_fonts.py deck.html \
      --sans  /path/NotoSansSC-Regular.otf  --sans-bold  /path/NotoSansSC-Bold.otf \
      --serif /path/NotoSerifSC-Bold.otf \
      -o deck.offline.html

说明：
  - 只抽取用到的字，通常每个字重 200–600 KB；不用的字重可以不传。
  - 生成后会去掉 Google Fonts 链接，并把字体放到字体栈第一位（所有主题都生效）。
  - 字体授权请自行确认：思源 / Noto 字体为 SIL OFL，可以内嵌。
"""
import argparse, base64, io, re, sys

def subset(path, text, index=0):
    from fontTools import subset as fs
    from fontTools.ttLib import TTFont
    opts = fs.Options(); opts.flavor = None; opts.layout_features = ['*']; opts.name_IDs = ['*']; opts.notdef_outline = True
    try:
        import brotli  # noqa
        opts.flavor = 'woff2'; fmt = 'woff2'
    except ImportError:
        opts.flavor = 'woff'; fmt = 'woff'
    font = TTFont(path, fontNumber=index)
    sub = fs.Subsetter(opts); sub.populate(text=text); sub.subset(font)
    buf = io.BytesIO(); font.flavor = opts.flavor; font.save(buf)
    return base64.b64encode(buf.getvalue()).decode(), fmt, len(buf.getvalue())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('file'); ap.add_argument('-o', '--out')
    ap.add_argument('--sans'); ap.add_argument('--sans-bold'); ap.add_argument('--serif'); ap.add_argument('--serif-regular')
    ap.add_argument('--index', type=int, default=0, help='.ttc 字体集合里的序号（例如 Noto CJK 的简体中文）')
    a = ap.parse_args()
    html = open(a.file, encoding='utf-8').read()
    body_text = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', html, flags=re.S)
    body_text = re.sub(r'<[^>]+>', ' ', body_text)
    text = ''.join(sorted(set(body_text))) + ''.join(chr(c) for c in range(32, 127)) + '，。、；：？！“”‘’（）《》—…·→←↑↓×÷±≤≥①②③④⑤⑥⑦⑧⑨⑩'
    faces, total = [], 0
    for fam, weight, path in (('DeckKit Sans', 400, a.sans), ('DeckKit Sans', 700, a.sans_bold), ('DeckKit Serif', 400, a.serif_regular), ('DeckKit Serif', 700, a.serif)):
        if not path: continue
        b64, fmt, n = subset(path, text, a.index); total += n
        faces.append("@font-face{font-family:'%s';font-weight:%d;font-display:swap;src:url(data:font/%s;base64,%s) format('%s')}" % (fam, weight, fmt, b64, fmt))
        print(f'{fam} {weight}: {n/1024:.0f} KB  ← {path}')
    if not faces:
        sys.exit('至少传一个字体：--sans / --sans-bold / --serif')
    html = re.sub(r'<link[^>]+fonts\.(googleapis|gstatic)\.com[^>]*>\s*', '', html)
    if a.sans or a.sans_bold:
        html = re.sub(r'(--f-body:)', r"\1'DeckKit Sans',", html)
    if a.serif or a.serif_regular:
        html = re.sub(r'(--f-display:)', r"\1'DeckKit Serif',", html)
    html = html.replace('<style>', '<style>' + ''.join(faces), 1)
    out = a.out or re.sub(r'\.html?$', '', a.file) + '.offline.html'
    open(out, 'w', encoding='utf-8').write(html)
    print(f'已写入 {out}（新增字体约 {total/1024:.0f} KB，字数 {len(set(text))}）')

if __name__ == '__main__':
    main()
