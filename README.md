# Send it home

A one-minute game for children of any age, played on a phone at an event booth.
The child helps a seafarer send money from one card to another: **enter an
amount, enter the recipient's Customer ID, send.** At the end they get a code to
show at the booth in exchange for a small token.

**Play it:** https://k8000xx.github.io/send-it-home/

`index.html` is the booth game — one self-contained file. No build, no server, no
dependencies, no data collected, and nothing stored between plays.

## What the child does

| | Screen | Action |
| --- | --- | --- |
| | Welcome | Meets Ana, a ship's cook, and her crew card — already loaded with $900 |
| 1 | How much? | Taps an amount on a big keypad, or picks $100 / $300 / $600 |
| 2 | Who gets it? | Types the family's six-digit Customer ID, copying it from the card on screen |
| 3 | Ready to send? | Checks from / to / amount / fee, presses **Send** |
| | Sent | Money flies card to card, receipt appears, reward code appears |

Everything else is flavour, kept to two short lines: **Ana's employer — the
shipping company she works for — puts her wages straight onto her card**, so
there is no cash to carry and no bank to visit. The transfer itself is card to
card: instant, no fee.

Deliberately forgiving, because the players are small and the queue is long:

- A wrong digit in the Customer ID is simply not accepted — a shake and a buzz,
  nothing lost. After two misses the game highlights the next digit to copy.
- Sending more than is on the card turns the amount red and disables **Next**.
- A back arrow on every step, and **Play again** at the end.
- No typing on the phone keyboard anywhere: big on-screen keys only.

## Running the booth

### Booth knobs live in the URL

- `?day=DOLPHIN` — today's word, shown on the finish screen
- `?id=482013` — a different six-digit Customer ID (anything invalid falls back
  to `730419`)
- combined: `?day=DOLPHIN&id=482013`

### Print the poster

`scripts/make-poster.py` builds a print-ready poster with the QR code baked in as
an inline SVG:

```bash
pip install segno
python3 scripts/make-poster.py "https://k8000xx.github.io/send-it-home/" --day DOLPHIN
```

That writes `booth-poster.html` — open it in a browser and print. Options:
`--day WORD` (added to the encoded URL and printed for staff), `--size a4|letter|a5`,
`--ecc m|h` (error correction), `--out FILE`.

The poster carries the title, the QR, the three steps, the prize line and the URL
in small print, so a phone that will not scan can still be typed at.

### Checking a finished game

The child shows a screen with a code like `SM-HJKT`, today's word, and a clock
that is *ticking*. A screenshot has a frozen clock and, if the word changes daily,
the wrong word. The code itself is random per play; it is a token to hand over,
not a password.

Phones need a connection to load the page once. After that the game runs entirely
in the browser, so flaky booth wifi mid-game will not break it.

## Also here

`classroom.html` is a longer version — five stops covering a seafarer's whole pay
cycle (signing on, wages at sea, the monthly allotment home, comparing transfer
options, and budgeting at home) with a printable certificate. About ten minutes,
better suited to a classroom or a quiet table than a booth queue.

## Brand and figures

The palette is a placeholder, defined in one labelled block of CSS custom
properties at the top of each HTML file:

```css
--navy  --blue  --aqua  --gold  --sand
```

Replace those hex codes and the whole game re-skins. The wordmark is plain text,
not a logo.

Every figure is invented for the game — the $900 wage, the $0 card-to-card fee,
the names, the Customer ID. They are illustrative, not anyone's real rates.
