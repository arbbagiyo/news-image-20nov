[![make.fun](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/arbbagiyo/news-image-20nov/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/arbbagiyo/news-image-20nov/reward.svg)](https://make.fun/bounty/news-image-20261120)

# The World — Friday 20 November 2026

Built for the [make.fun bounty "Sum up 20 November's world news in one image"](https://make.fun/bounty/news-image-20261120).

A newspaper front page drawn programmatically with Python + PIL (`render.py`),
1024×1024 PNG. Masthead "THE WORLD", red dateline "FRIDAY, 20 NOVEMBER 2026":

- **Main story:** Russian missiles hit Poland — two missiles and a jet-powered
  drone crash in south-east Poland; Warsaw calls it a deliberate provocation,
  NATO jets scramble.
- **Second story:** Stocks plunge as the AI rally cracks — S&P 500 down 3.7%
  into correction, Nikkei down 5.1%; Nvidia faces an SEC probe.
- **Also:** COP31 climate talks in overtime, Trump threatens a tech tax,
  US loses measles-free status, Palisades fire verdict — plus Anthropic's IPO
  debut, the EU–UK summit and a 6.7 quake in Peru.

## How it runs

`main.ts` (Node 22, standard library only) copies `entry.png` to
`/output/entry.png`. Two runs are byte-identical:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

Re-render the image from scratch with:

```sh
python3 render.py
```

## License

MIT — see `LICENSE`.
