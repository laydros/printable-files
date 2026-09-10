# printable-files

Generates printable 3x5 index cards for an analog task system, plus 4-up
letter-size sheets for printing them in batches.

Three card types, each identical except for the title:

- **Today** — what you're working on now
- **Next** — what's queued up
- **Someday** — what you might get to eventually

Each card has a title, three checkboxes and a date rule in the top right, and
ten task lines. Every task line gets a circle with a vertical tick through it
on the left and a gray rule to write on.

## Setup

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Usage

```sh
.venv/bin/python generate-analog.py
```

That regenerates every PDF in one pass. Output goes to two directories, both
tracked in git:

- `cards/` — one 3x5 PDF per card type, sized exactly to the card
- `sheets/` — one 8.5x11 PDF per card type, four cards to a page with crop
  marks for trimming

The 4-up sheets are laid out so adjacent cards share a cut line, which means
fewer passes with the trimmer.

Re-running the generator always shows all six PDFs as modified in git, even
when nothing about the layout changed. reportlab stamps a creation timestamp
and a producer string into every file, which is roughly 60 bytes of difference
per PDF. Unless you actually changed the drawing, revert them:

```sh
git checkout -- cards/ sheets/
```

To tell a real change from that noise, compare the decompressed content
streams rather than the raw bytes. The drawing operators live there and the
metadata does not.

## Layout tweaks

All the geometry lives in the `layout` dict near the top of
`generate-analog.py` — card size, margins, checkbox radius, line spacing.
Change a value there and re-run to see it.

`draw_card_to_canvas` draws a single card at the current canvas origin, so
both the individual cards and the 4-up sheets go through the same code. If you
change how a card looks, both outputs stay in step.

## Fonts

Inter (Regular and Bold) ships in `fonts/` so the output does not depend on
what is installed locally. Inter is licensed under the SIL Open Font License.
