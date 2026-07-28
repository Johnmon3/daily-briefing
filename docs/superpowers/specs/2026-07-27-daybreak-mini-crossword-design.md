# Daybreak Mini — daily mini crossword design

**Date:** 2026-07-27
**Status:** Approved (design); implementation pending

## Overview

Add a daily mini crossword ("The Mini") to the bottom of the Daybreak full
briefing page (`briefing/index.html`). It is a **static** puzzle (solve in your
head / on paper) with a **no-JavaScript** answer reveal, drawn each day from a
**pre-built, verified bank** of puzzles that rotate by date. This keeps every
puzzle guaranteed-valid and adds negligible cost to the morning routine.

## Decisions (locked)

- **Interactivity:** Static grid + reveal (no live typing).
- **Reveal mechanism:** Native HTML `<details>` — no JS, renders in both the
  claude.ai artifact and the htmlpreview public page.
- **Content:** General-knowledge, timeless clues (not news-themed).
- **Generation:** Approach A — pre-built, hand-verified puzzle bank; the routine
  only selects and pastes the day's puzzle. No runtime construction.
- **Email:** Page-only puzzle. Add a one-line teaser in the email linking to the
  page (email clients strip `<details>`, so the puzzle itself cannot live there).
- **Bank size:** Launch with **20** puzzles (`BANK_SIZE = 20`), ~3 weeks before a
  repeat. Extensible by adding files and bumping `BANK_SIZE`.

## Components

### 1. Puzzle bank — `briefing/minis/NN.html`
- Files `01.html` … `20.html`, each a self-contained static block for one puzzle.
- Each block contains: the 5x5 grid, numbered Across/Down clue lists, and the
  answer key wrapped in `<details>`.
- Blocks use only CSS classes defined in `index.html`'s `<style>` (no inline
  styles, no scripts).
- **Validity is a hard requirement:** for every puzzle, each Across entry AND
  each Down entry must be a real word, and every clue must match its answer.
  Each puzzle is verified during construction (enumerate all across/down entries
  and confirm they are words).

### 2. Grid format
- 5x5 grid rendered with CSS grid. Cells are either:
  - **letter cells** — empty for solving, with a small clue number in the corner
    where an entry begins; or
  - **block cells** — filled (`--ink`), non-writable.
- Standard mini style (a few block cells), ~5 Across and ~5 Down entries.
- Reveal (`<details>`) shows the **completed grid** (filled letters).

### 3. Placement & nav
- New `<section class="mini" id="mini" data-mini-id="NN">` placed **after the
  Finance topic section and before the `.signoff` footer**.
- Add "The Mini" as the last link in the masthead `topic-nav` (`#mini`).

### 4. Styling
- One `/* ---------- Mini crossword ---------- */` block added to
  `index.html`'s `<style>`, using existing theme vars (`--card`, `--hairline`,
  `--ink`, `--muted`, `--faint`, `--accent`). Light/dark aware.
- Classes (indicative): `.mini`, `.mini-head`, `.mini-grid`, `.mini-cell`,
  `.mini-cell.block`, `.mini-num`, `.mini-clues`, `.mini-col`, `.mini-answer`.
- The routine already preserves the entire `<style>` block, so this persists.

### 5. Daily selection (routine)
- The routine computes the index with a **shell command**, not LLM arithmetic:
  `N = (days_since_epoch mod BANK_SIZE) + 1`, zero-padded to two digits, e.g.
  `NN=$(printf '%02d' $(( ($(date -u +%s)/86400) % 20 + 1 )))`.
- It reads `briefing/minis/$NN.html` and pastes the contents **verbatim** inside
  `<section ... id="mini"> ... </section>`, replacing the prior puzzle, and sets
  `data-mini-id="NN"`. It must not alter the puzzle HTML.
- Added as a new numbered step in the routine prompt; the puzzle is NOT part of
  the news research and does not change token cost meaningfully.

### 6. Email teaser
- In `briefing/email.html`, add a single small line near the "Read the full
  briefing" button: `🧩 Today's Mini crossword is waiting at the foot of the
  briefing.` No grid, no answers in the email.
- Routine prompt updated to keep this teaser line.

## Out of scope
- Live/typeable grid, scoring, timers, saving progress.
- News-themed or freshly-generated puzzles.
- Puzzle content in the email body.

## Refill process
- When the bank is near a full rotation (or on request), add `21.html`, `22.html`,
  … and bump `BANK_SIZE` in the routine's selection command. No other changes.

## Launch / verification
- Add CSS + an initial puzzle inlined into today's `index.html` so it shows on
  the current page immediately (not only next morning).
- Verify: grid renders in light and dark; `<details>` reveals the completed grid
  in both artifact and htmlpreview; nav link scrolls to the section; email teaser
  present; routine prompt selects and inlines the correct daily file.
