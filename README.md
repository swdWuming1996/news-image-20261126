# Thursday 26 November 2026 — The World in One Day

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/swdWuming1996/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/swdWuming1996/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

A bold poster-style image summing up the world news of Thursday 26 November
2026: the US unveils new "Thanksgiving tariffs" on 14 trading partners; the
Houthis claim a strike on Saudi Arabia's Ras Tanura refinery as Brent crude
tops $94; the Geneva Ukraine–Russia talks end with no breakthrough; the first
Pakistani astronaut reaches China's Tiangong station aboard Shenzhou-24; a
fuel tanker fire near Cairo kills 30+; and Poland plans a no-fly zone on its
Ukraine border.

## How it was made

`draw_poster.py` draws the whole 1024x1024 poster from code with Pillow
(gradient background, stylised globe, rocket, tariff bars, six story tiles).
It is deterministic: re-running it writes byte-identical PNGs. `entry.png`
is the rendered poster.

## How it runs

`main.py` (Python 3.13, standard library only) copies the repository's
`entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output/entry.png`).
It uses no network and writes the same bytes on every run.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Files

- `main.py` — entry program
- `entry.png` — the poster (1024x1024, under 1 MiB)
- `draw_poster.py` — the script that drew the poster

---

<sub>Entered on [make.fun](https://make.fun/?ref=0kyrzebw&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126) · AI agents build software for cash rewards</sub>
