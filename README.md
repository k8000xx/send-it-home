# Send it home

A one-minute game for children of any age, played on a phone at an event booth.
The child helps a seafarer send money from one card to another: **enter an
amount, enter the recipient's Customer ID, send.** At the end they get a code to
show at the booth in exchange for a small token.

**Play it:** https://k8000xx.github.io/send-it-home/

`index.html` is the booth game — one self-contained file. No build, no server, no
dependencies, no data collected, and nothing stored between plays.

## What the child does

They meet Ana, a ship's cook, whose crew card is already loaded with $900, then
pick one of two ways to send money home. Either way is three steps and about a
minute, and both end at the same reward code — so a child who plays twice gets
the other one.

**Card to card** — instant, no fee:

| | Screen | Action |
| --- | --- | --- |
| 1 | How much? | Taps an amount on a big keypad, or picks $100 / $300 / $600 |
| 2 | Who gets it? | Copies the family's Customer ID from the card — the leading `00` is filled in, so eight digits to type |
| 3 | Ready to send? | Checks from / to / amount / fee, presses **Send** |

**Wire to a bank** — a small fee, one to two days:

| | Screen | Action |
| --- | --- | --- |
| 1 | Add a recipient | Name, bank, SWIFT/BIC and account are already filled in; the child checks them and saves |
| 2 | How much? | Same keypad, but the amount has to cover the $8 wire fee |
| 3 | Your quotation | Sees the fee taken off, the exchange rate applied, and exactly what Maria receives in pesos, then presses **Send funds** |

The two paths are the lesson: the same money, sent two ways, with the cost and
the waiting laid side by side. The quotation is where that lands — a child can
read that $150 becomes ₱8,264.40 after an $8 fee, and that it takes a day or two,
while the card transfer arrives before they put the phone down.

Everything else is flavour, kept to two short lines: **Ana's employer — the
shipping company she works for — puts her wages straight onto her ShipMoney
card**, so there is no cash to carry and no bank to visit.

Deliberately forgiving, because the players are small and the queue is long:

- The Customer ID is ten digits, but the leading `00` arrives already filled in
  and cannot be deleted, so a child types eight. It is shown and entered in
  groups — `00 7304 1982` — to be read a chunk at a time rather than as one run.
- A wrong digit is simply not accepted — a shake and a buzz, nothing lost. After
  two misses the game highlights the next digit to copy.
- Sending more than is on the card turns the amount red and disables **Next**.
- A back arrow on every step, and **Play again** at the end.
- No typing on the phone keyboard anywhere: big on-screen keys only.
- Sounds are short beeps; phones that support it also give a light buzz.

## Running the booth

### Booth knobs live in the URL

- `?day=DOLPHIN` — today's word, shown on the finish screen
- `?id=0048201374` — a different Customer ID. Ten digits opening with `00`;
  anything else falls back to `0073041982`
- combined: `?day=DOLPHIN&id=0048201374`

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
the $8 wire fee, the ₱58.20 exchange rate, the names, the Customer ID, and the
bank and its SWIFT code (Ocean Bank / OCBKPHMM is not a real bank). They are
illustrative, not anyone's real rates.
