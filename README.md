# 21 November 2026 — The World in One Day

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/zdoo8866-design/makefun-news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/zdoo8866-design/makefun-news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

![The front page: six panels summing up 21 November 2026](entry.png)

One 1024×1024 front page that sums up a single day of world news —
**21 November 2026**, named in large type at the top. Six panels in a
2×3 grid over one shared pale backdrop (a dawn sky over a calm sea),
each with a drawn scene, a location tag, a headline, one line of fact,
and the day's key number as a chip. The palette stays plain on purpose;
colour is spent only on details — sparks in a tanker's plume, the amber
screen in Geneva, the red critical line on a chalkboard, the yellow
slides on a night tarmac.

## The six stories

1. **Strait of Hormuz — Two tankers hit in the strait** · chip: *2 tankers hit*
   Two outbound tankers are struck by unidentified projectiles off
   Khasab, Oman, on Saturday morning — the second in its engine room,
   about 50 minutes after the first. No casualties in either incident,
   UKMTO says.
   Sources: Reuters; The Jerusalem Post; UKMTO warnings 215-26.
2. **Geneva — 'Killer robot' talks end with a path, no pact** · chip: *rules by 2028*
   The CCW review conference ends after 4 a.m. on Saturday: 128 states
   agree to spend two years elaborating an instrument on lethal
   autonomous weapons. About 100 countries wanted binding rules; the
   US, Russia and Israel held out, so whether the rules will bind is
   left open.
   Sources: Reuters; AFP.
3. **Antalya — COP31 runs into overtime, still no deal** · chip: *COP32: Addis Ababa*
   The UN climate summit runs into an extra day with no final deal:
   work crews pack up the venue while negotiators chase a third draft
   that still omits any mention of fossil fuels. Ethiopia is confirmed
   as host of COP32 in Addis Ababa in 2027.
   Sources: Associated Press; Reuters.
4. **Basra — Power-station fire kills at least four** · chip: *800 MW offline*
   A fire breaks out around 6 a.m. at the Hartha power station north of
   Basra, spreads to nearby houses and shuts the plant. At least four
   people are killed and 30 injured, officials say; the cause is not
   yet known.
   Sources: Reuters; Al Jazeera.
5. **Cambridge, Mass. — Race to verify the Riemann claim** · chip: *167 years open*
   A day after an Anthropic researcher published a claimed,
   AI-assisted proof of the Riemann hypothesis as some 17 million
   lines of Lean, independent teams at MIT and Carnegie Mellon compile
   it successfully. Deeper checks for trickery continue — and a rival,
   all-human proof surfaces the same day. Nothing is settled yet.
   Sources: Quanta Magazine; The Wall Street Journal; AFP.
6. **Davao — Everyone walks away from flight PX19** · chip: *146 safe*
   Air Niugini flight PX19, a Boeing 767 from Hong Kong to Port
   Moresby, diverts to Davao shortly after midnight after a fire
   warning in its right engine. All 137 passengers and 9 crew leave by
   the emergency slides; no one is hurt.
   Sources: Associated Press; Channel NewsAsia.

Every story is an event of 21 November 2026 (in its local time zone),
cross-checked against at least two reliable reports before it was
drawn. Several of the day's biggest headlines were left out on
purpose: the UK–EU reset summit, the Danish expulsion over a foiled
plot, the overnight barrage on Ukraine and the pancreatic-cancer
trial results all turned out, on inspection, to be events of
20 November that Saturday's papers were still leading with.

## How it was made

The backdrop and the six scenes were drawn as separate illustrations
in one consistent flat watercolour style, with no text in the artwork
itself; they live in `art/`. All type — the date, headlines, fact
lines, tags and number chips — was then set programmatically over the
artwork by `tools/compose.py`, so every word and figure is exact and
legible. A one-line inventory runs along the bottom: *a strait struck ·
a pact postponed · a summit in overtime · a fatal fire · a proof to
check · a safe landing*.

## Run it

```sh
bun run main.ts
```

`main.ts` verifies `entry.png` against the intake limits (PNG
signature, IHDR dimensions at most 1024×1024, at most 1 MiB), stages
it into `$MAKEFUN_OUTPUT_DIR` (falling back to `/output`, since the
repository is mounted read-only), and confirms the staged copy is
byte-identical by SHA-256.

## License

MIT — see [LICENSE](LICENSE).
