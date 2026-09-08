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

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Booth poster — Send it home</title>
<style>
  @page {{ size: {page}; margin: 12mm; }}
  :root {{ --navy:#062b4e; --blue:#0072ce; --aqua:#00b7c3; --gold:#ffb81c; }}
  *{{ box-sizing:border-box }}
  body{{
    margin:0; font-family:"Trebuchet MS","Segoe UI",system-ui,sans-serif; color:var(--navy);
    display:flex; justify-content:center; background:#e9f2f9;
  }}
  .sheet{{
    width:{width}; min-height:{height}; background:#fff; padding:16mm 14mm;
    display:flex; flex-direction:column; align-items:center; text-align:center;
  }}
  .lockup{{ display:flex; align-items:center; gap:10px; margin-bottom:4mm }}
  .lockup .mark{{ width:44px; height:44px; border-radius:12px; display:grid; place-items:center;
                 background:linear-gradient(140deg,var(--blue),var(--navy)); color:#fff; font-size:1.4rem }}
  .lockup b{{ font-size:1.6rem }}
  h1{{ font-size:clamp(2.4rem,7vw,3.4rem); margin:2mm 0 1mm; line-height:1.05 }}
  h2{{ font-size:1.5rem; margin:0 0 6mm; font-weight:normal; color:#41627c }}
  .qrbox{{ border:6px solid var(--navy); border-radius:18px; padding:6mm; background:#fff }}
  .qrbox svg{{ display:block; width:{qrsize}; height:{qrsize} }}
  .cta{{ font-size:1.7rem; font-weight:bold; margin:6mm 0 2mm }}
  .steps{{ display:flex; gap:6mm; justify-content:center; margin:4mm 0 0; flex-wrap:wrap }}
  .step{{ flex:1 1 0; min-width:52mm; max-width:62mm; background:#f4f7fa; border:2px solid #dbe7f0;
          border-radius:14px; padding:5mm 4mm }}
  .step .n{{ display:inline-grid; place-items:center; width:30px; height:30px; border-radius:50%;
            background:var(--gold); font-weight:bold; margin-bottom:2mm }}
  .step b{{ display:block; font-size:1.1rem }}
  .step span{{ font-size:.92rem; color:#41627c }}
  .prize{{ margin-top:6mm; background:#fff8e6; border:3px solid var(--gold); border-radius:16px;
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
    <div class="lockup"><div class="mark">⚓</div><b>ShipMoney</b></div>
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
    svg = qr.svg_inline(border=2, dark="#062b4e", omitsize=True)

    wordline = (
        f'<div style="margin-bottom:2mm">For booth staff — today\'s word is '
        f'<span class="word">{html.escape(day)}</span>, and the finish screen\'s clock ticks.</div>'
        if day else
        '<div style="margin-bottom:2mm">For booth staff — the finish screen shows a code '
        'and a clock that ticks; a screenshot does not.</div>'
    )

    page = PAGES[args.size]
    out = TEMPLATE.format(qr=svg, shown_url=html.escape(url), wordline=wordline, **page)
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
