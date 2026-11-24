# THE WORLD — Tuesday, 24 November 2026

[![make.fun](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/s8fr2hf/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/s8fr2hf/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

A newspaper front page summing up the world news of Tuesday, 24 November 2026 — drawn entirely with Pillow primitives and DejaVu fonts, no photographs.

## The stories on the page

- **Lead — Ukraine war:** President Volodymyr Zelenskyy said Ukrainian naval drones sank a Russian corvette in a Libyan port, a day after a drone struck a Russian-linked cargo ship in the Gulf of Finland. (Reuters, BBC)
- **Business — Tech:** Washington blacklisted Singapore chip firm Megaspeed over the Nvidia chip scandal. (Reuters)
- **Europe — Sanctions:** Brussels unveiled a new sanctions package hitting Russian banks, the shadow fleet and Russian athletes. (Reuters)
- **Ukraine war:** President Volodymyr Zelenskyy said intelligence shows Russia is preparing new strikes on Ukraine. (Reuters)
- **Asia — Indonesia:** at least 24 people died in a factory fire, with dozens still missing. (Reuters)
- **Europe — Baltic:** Moscow accused Estonia of hostile acts on the "verge of triggering open war". (Reuters)

## How it works

`render.py` draws the 1024×1024 front page: masthead and dateline, a drawn harbour scene for the lead story, and five further stories with small drawn icons (chip, ban sign, warning triangle, flame, flag). `main.py` (standard library only) re-renders the image, validates it (PNG, ≤ 1 MiB, 1024×1024) and writes it to `$MAKEFUN_OUTPUT_DIR/entry.png`.

## Run it

```sh
python3 main.py
```

Two runs produce byte-identical output.

## License

MIT — see `LICENSE`.
