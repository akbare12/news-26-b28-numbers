# The World in One Page — Thursday 26 November 2026

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/akbare12/news-26-b28-numbers/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/akbare12/news-26-b28-numbers/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

**50 stories. One image. Thursday 26 November 2026.**

## Layout V26

Three heroes stacked down the left 45% column, a 2×5 card grid in the
right 55% column, and a full-width bottom band: world map on the left (40%)
beside a three-column ALSO list on the right (60%). The map carries 12
numbered pins (New York, Hormuz, Washington, Gaza, Kyiv, Bogor, Jerusalem,
Pyongyang, London, Moscow, Bangkok, Cologne) with a legend. Masthead and a
two-line DATE CHECK on top, timeline strip and sources footer below.

## The three heroes

1. **NEW YORK [C] — Macy's 100th Thanksgiving Parade postponed.** A huge
   East Coast storm forces the first weather delay in the parade's 100-year
   history. Rescheduled Sat 28 Nov, 08:30 ET.
2. **HORMUZ [CL] — IRGC claims 2 tankers hit by mines.** Iran's
   Revolutionary Guard says two tankers, one a supertanker carrying over 2M
   barrels, exploded and burned near Khasab. The claim is unverified.
3. **GLOBAL MARKETS [C] — Trump tariffs: markets rebound.** Europe and Asia
   rally as the new tariff salvo on 14 partners looks milder than feared and
   will not stack on July tariffs. STOXX +1.6%.

## Cards (10)

Gaza, Kyiv, Bogor (13 dead, 13 missing in a flooded illegal gold mine),
Jerusalem, Pyongyang, Washington (FCC clears SpaceX 1M-satellite data
centres), London (UK net migration 77,000), Moscow, Bangkok (oil depot
blast, 7 injured), Cologne (2 held over a synagogue plot).

## ALSO today (37 more stories)

Philadelphia parade cancelled, NBC airs the 2025 parade, UKMTO warnings off
Dubai and Khasab, Ras Tanura claim (25 Nov), OPEC+ meets 29 Nov, Brent
$93.8, gold $3,572/oz, Nvidia −3.91%, Norse Atlantic suspends all flights,
Poundland enters administration, Malaysia sues Google for $146m, and more —
every item tagged [C] confirmed or [CL] claim.

## Date check

Every story is verified for **Thu 26 Nov 2026**. Events from 25 Nov are
dated in the text (tariff announcement, FCC approval, Ras Tanura strike).
Sources: Reuters, AP, BBC, CNN, NPR, UKMTO, ONS, KCNA.

## How it is built

- `gen.py` renders `entry.png` (1024×1024) with Pillow at build time. All
  text is measured against its real column width; nothing is truncated.
- `main.py` is **stdlib-only**: it copies the pre-rendered `entry.png` to
  `$MAKEFUN_OUTPUT_DIR/entry.png` and verifies the copy by sha256.

## Verification

- `entry.png`: 1024×1024, 233366 bytes
- sha256: `85a3c7bf53cd0647b0a992a7a432a4d8dee64d8b06b83b272a4b4043d068004c`
- Stories: 50 (3 heroes + 10 cards + 37 ALSO)
- Duplicate scan (≥3 distinctive words shared between any two items): 0 flags
- Stdlib-venv simulation: exit 0, output sha matches the committed image
