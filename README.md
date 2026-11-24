[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Donnyp21/entry-news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/Donnyp21/entry-news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

# news-image-20261124 — Tuesday 24 November 2026, in one image

A newspaper front page, "TUESDAY 24 NOVEMBER 2026", that packs the day's world news into a single frame. Every story was verified against reporting dated 24 Nov 2026 by web search:

1. **Ukraine's drones sink a Russian warship in Libya** — sea drones sank the corvette Merkury at the Benghazi naval base on 23 Nov; Libya demands answers, the UN seeks a probe.
2. **Russia tests NATO skies** — 25 airspace violations against NATO members in 2026, four times the 2024 total; two missiles and a drone fell in Poland on 20 Nov.
3. **14 nations back the ICJ Rohingya ruling** — the UK, Spain, Canada, Australia and 10 more recognise the ruling that Myanmar committed genocide against the Rohingya.
4. **Stocks surge as Nvidia reinstates Huang** — Kospi +6–7%, Nikkei +3.9%, Nasdaq +6.5%, S&P 500 +4.7% after Trump intervened.
5. **US sanctions dozens of Iran exchange houses** — the Treasury sanctions 24+ Iranian exchange houses amid Hormuz tensions; Tehran sets 7 conditions for talks.
6. Also today: Putin reportedly open to Article 5-style security guarantees for Ukraine if no NATO troops deploy · COP31 collapsed in Antalya over fossil-fuel wording (first failure since 2009; COP32 to Addis Ababa) · Nepal quake 5.6 near the China border · factory fire in Cikande, Indonesia, with casualties · 9th measles death in Pennsylvania.

## How it works

`gen_image.py` (build-time only, Pillow) paints the artwork from scratch — shapes and text, no photographs, no copied artwork — and saves it as `art.jpg` (1024x1024 JPEG). `main.py` (Python 3.13 standard library only, no network) checks that artwork against the competition's caps (a whole JPEG, at most 1 MiB, at most 1024x1024 pixels) and copies it to `$MAKEFUN_OUTPUT_DIR/entry.png` (falling back to `$MAKEFUN_OUTPUT`, then `/output`). The output is a byte-for-byte copy, so two runs produce identical bytes.

Run: `MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py`
Regenerate the artwork: `python3 gen_image.py`
