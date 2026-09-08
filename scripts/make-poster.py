#!/usr/bin/env python3
"""Build a printable booth poster with the game's QR code baked in.

    pip install segno
    python3 scripts/make-poster.py "https://example.com/games/seafarer-earnings/index.html" \
        --day DOLPHIN --out booth-poster.html

Then open the poster in a browser and print it. The QR is an inline SVG, so it
stays sharp at any size and the poster needs no internet connection.
"""
import argparse
import html
import re
import sys
from urllib.parse import urlencode, urlparse, urlunparse, parse_qsl

try:
    import segno
except ImportError:
    sys.exit("segno is not installed.  Run:  pip install segno")

# Official ShipMoney lockup (dark), cut from ShipmoneyLogoDARKBLUELIGHTBLUE.png
LOGO = "data:image/png;base64,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"

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Booth poster — Send it home</title>
<style>
  @page {{ size: {page}; margin: 12mm; }}
  :root {{ --navy:#002F71; --blue:#00389F; --cyan:#00B5E8; --ice:#79DFFF; }}
  *{{ box-sizing:border-box }}
  body{{
    margin:0; font-family:"Trebuchet MS","Segoe UI",system-ui,sans-serif; color:var(--navy);
    display:flex; justify-content:center; background:#e9f2f9;
  }}
  .sheet{{
    width:{width}; min-height:{height}; background:#fff; padding:16mm 14mm;
    display:flex; flex-direction:column; align-items:center; text-align:center;
  }}
  .lockup{{ margin-bottom:5mm }}
  .lockup img{{ width:62mm; max-width:80%; height:auto; display:block; margin:0 auto }}
  h1{{ font-size:clamp(2.4rem,7vw,3.4rem); margin:2mm 0 1mm; line-height:1.05 }}
  h2{{ font-size:1.5rem; margin:0 0 6mm; font-weight:normal; color:#41627c }}
  .qrbox{{ border:6px solid var(--navy); border-radius:18px; padding:6mm; background:#fff }}
  .qrbox svg{{ display:block; width:{qrsize}; height:{qrsize} }}
  .cta{{ font-size:1.7rem; font-weight:bold; margin:6mm 0 2mm }}
  .steps{{ display:flex; gap:6mm; justify-content:center; margin:4mm 0 0; flex-wrap:wrap }}
  .step{{ flex:1 1 0; min-width:52mm; max-width:62mm; background:#f4f7fa; border:2px solid #dbe7f0;
          border-radius:14px; padding:5mm 4mm }}
  .step .n{{ display:inline-grid; place-items:center; width:30px; height:30px; border-radius:50%;
            background:var(--cyan); color:#fff; font-weight:bold; margin-bottom:2mm }}
  .step b{{ display:block; font-size:1.1rem }}
  .step span{{ font-size:.92rem; color:#41627c }}
  .prize{{ margin-top:6mm; background:#E8F6FE; border:3px solid var(--cyan); border-radius:16px;
           padding:4mm 6mm; font-size:1.25rem; font-weight:bold }}
  .foot{{ margin-top:auto; padding-top:6mm; font-size:.8rem; color:#6b859a; width:100% }}
  .foot code{{ font-size:.78rem; word-break:break-all }}
  .word{{ display:inline-block; background:var(--navy); color:#fff; border-radius:8px;
          padding:2px 12px; letter-spacing:.14em; font-weight:bold }}
  @media print{{ body{{ background:#fff }} .sheet{{ width:auto; min-height:auto; padding:0 }} }}
</style>
</head>
<body>
  <div class="sheet">
    <div class="lockup"><img src="{logo}" alt="ShipMoney"></div>
    <h1>Send it home</h1>
    <h2>Help a sailor at sea send money to their family</h2>

    <div class="qrbox">{qr}</div>
    <div class="cta">📱 Scan to play — one minute</div>

    <div class="steps">
      <div class="step"><div class="n">1</div><b>Choose an amount</b><span>How much goes home?</span></div>
      <div class="step"><div class="n">2</div><b>Type the Customer ID</b><span>The family's card number</span></div>
      <div class="step"><div class="n">3</div><b>Send it</b><span>Card to card — instant, free</span></div>
    </div>

    <div class="prize">🎁 Finish the game and show your code here for a prize</div>

    <div class="foot">
      {wordline}
      <div><code>{shown_url}</code></div>
    </div>
  </div>
</body>
</html>
"""

PAGES = {
    "a4":     {"page": "A4",     "width": "210mm", "height": "297mm", "qrsize": "78mm"},
    "letter": {"page": "Letter", "width": "216mm", "height": "279mm", "qrsize": "78mm"},
    "a5":     {"page": "A5",     "width": "148mm", "height": "210mm", "qrsize": "58mm"},
}


def with_day(url: str, day: str) -> str:
    """Put ?day=WORD on the URL, replacing any day already there."""
    parts = urlparse(url)
    query = [(k, v) for k, v in parse_qsl(parts.query) if k != "day"]
    query.append(("day", day))
    return urlunparse(parts._replace(query=urlencode(query)))


def main() -> None:
    ap = argparse.ArgumentParser(description="Build a printable booth poster with a QR code.")
    ap.add_argument("url", help="Public URL where index.html is hosted")
    ap.add_argument("--day", default="", help="Today's word, printed on the finish screen (A-Z 0-9)")
    ap.add_argument("--out", default="booth-poster.html", help="Output file (default: booth-poster.html)")
    ap.add_argument("--size", choices=sorted(PAGES), default="a4", help="Paper size (default: a4)")
    ap.add_argument("--ecc", choices=["l", "m", "q", "h"], default="m",
                    help="Error correction: m (default) is standard for URLs and keeps the QR "
                         "chunky and easy to scan; h survives more scuffing but packs in more, "
                         "smaller squares")
    args = ap.parse_args()

    url = args.url.strip()
    if not urlparse(url).scheme:
        sys.exit("The URL needs a scheme, e.g. https://…")

    day = re.sub(r"[^A-Z0-9]", "", args.day.upper())[:10]
    if day:
        url = with_day(url, day)

    qr = segno.make(url, error=args.ecc)
    # omitsize gives the <svg> a viewBox and no fixed width/height, so the CSS
    # below can scale it to the paper size without shrinking the code itself.
    svg = qr.svg_inline(border=2, dark="#002F71", omitsize=True)

    wordline = (
        f'<div style="margin-bottom:2mm">For booth staff — today\'s word is '
        f'<span class="word">{html.escape(day)}</span>, and the finish screen\'s clock ticks.</div>'
        if day else
        '<div style="margin-bottom:2mm">For booth staff — the finish screen shows a code '
        'and a clock that ticks; a screenshot does not.</div>'
    )

    page = PAGES[args.size]
    out = TEMPLATE.format(qr=svg, shown_url=html.escape(url), wordline=wordline, logo=LOGO, **page)
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(out)

    print(f"Wrote {args.out}")
    print(f"  URL       {url}")
    modules = qr.symbol_size(border=0)[0]
    mm = round(float(page["qrsize"].rstrip("m")) / modules, 2)
    print(f"  QR        version {qr.version}, {modules}x{modules} modules at {mm}mm each, "
          f"error correction {args.ecc.upper()}")
    print(f"  Paper     {page['page']}")
    print("Open it in a browser and print.")


if __name__ == "__main__":
    main()
