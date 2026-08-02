# Model value index for Artificial Analysis stats

## Recommendation

Use the **cost + speed index** as the final comparison column. It preserves the requested quality mix—40% intelligence and 60% coding—while penalizing both benchmark cost and response time. The cost-only index is useful as an intermediate check, but it can over-reward a cheap model even when that model is very slow.

The source CSV contains 28 models in rows 2–29. Its relevant columns are:

| Column | Field | Use |
|---|---|---|
| E | AA Intelligence Index | 40% of quality |
| F | AA Coding Index | 60% of quality |
| G | AA Benchmark Cost | Primary cost measure; lower is better |
| H | BlendedUSD/1M Tokens | Reference price only |
| I | AA TotalResponse (s) | Speed measure; lower is better |

`AA Benchmark Cost` is preferred over `BlendedUSD/1M Tokens` because it measures the cost of running the benchmark workload, not merely the listed price per token.

## 1. Weighted quality

For each model:

```text
Weighted quality = 0.40 × Intelligence + 0.60 × Coding
```

In row 2:

```excel
=0.4*E2+0.6*F2
```

This remains on approximately the same scale as the two source quality indexes.

## 2. Cost-adjusted index

The raw cost efficiency is:

```text
Cost efficiency = Weighted quality / Benchmark cost
```

Normalize it so the best model in the current table receives 100:

```excel
=100*((0.4*E2+0.6*F2)/G2)/MAX((0.4*$E$2:$E$29+0.6*$F$2:$F$29)/$G$2:$G$29)
```

Enter the formula in a new column on row 2 and fill down through row 29. A higher score is better.

The weakness of this rating is visible at the top: DeepSeek V4 Pro wins on cost efficiency despite taking 84.06 seconds, versus 5.47 seconds for GPT-5.6 Terra (medium).

## 3. Improved cost + speed index

Treat cost and time as equally important penalties using their geometric mean:

```text
Combined penalty = √(Benchmark cost × Response time)
Raw value = Weighted quality / Combined penalty
Final index = 100 × Raw value / highest Raw value in the table
```

The geometric mean is preferable to simply multiplying cost and time because it gives each penalty equal influence on a percentage-change basis without making the combined penalty excessively harsh.

Use this one-column formula in row 2 and fill down through row 29:

```excel
=100*((0.4*E2+0.6*F2)/SQRT(G2*I2))/MAX((0.4*$E$2:$E$29+0.6*$F$2:$F$29)/SQRT($G$2:$G$29*$I$2:$I$29))
```

## Full model table

The table is sorted by the recommended cost + speed rating. `Quality` is the 40% intelligence / 60% coding blend. The two **Rating** columns are the requested additions and are both normalized to a maximum of 100 across these 28 models.

| Final rank | Model | Intelligence | Coding | Quality | Benchmark cost | Response (s) | Cost rating | Cost + speed rating |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | GPT-5.6 Terra (medium) | 46 | 65 | 57.4 | 240.23 | 5.47 | 79.50 | 100.00 |
| 2 | GPT-5.6 Luna (high) | 46 | 63 | 56.2 | 275.02 | 6.79 | 67.99 | 82.13 |
| 3 | GPT-5.6 Terra (high) | 49 | 67 | 59.8 | 495.77 | 6.18 | 40.13 | 68.23 |
| 4 | GPT-5.6 Sol (low) | 49 | 70 | 61.6 | 353.49 | 9.66 | 57.98 | 66.57 |
| 5 | GPT-5.6 Sol (medium) | 54 | 76 | 67.2 | 593.04 | 11.96 | 37.70 | 50.39 |
| 6 | MiniMax-M3 | 44 | 59 | 53.0 | 203.86 | 27.27 | 86.50 | 44.89 |
| 7 | Grok 4.5 (high) | 54 | 72 | 64.8 | 600.92 | 19.39 | 35.88 | 37.91 |
| 8 | GPT-5.6 Sol (high) | 56 | 77 | 68.6 | 955.55 | 13.85 | 23.89 | 37.66 |
| 9 | GLM-5.2 (max) | 51 | 69 | 61.8 | 820.38 | 14.41 | 25.06 | 35.90 |
| 10 | GPT-5.6 Luna (xhigh) | 49 | 69 | 61.0 | 479.37 | 27.81 | 42.34 | 33.36 |
| 11 | GPT-5.5 (medium) | 50 | 72 | 63.2 | 869.91 | 17.12 | 24.17 | 32.71 |
| 12 | DeepSeek V4 Pro (max) | 44 | 59 | 53.0 | 176.34 | 84.06 | 100.00 | 27.49 |
| 13 | GPT-5.6 Terra (xhigh) | 52 | 71 | 63.4 | 740.21 | 31.06 | 28.50 | 26.41 |
| 14 | Gemini 3.1 Pro Preview | 46 | 69 | 59.8 | 815.11 | 30.04 | 24.41 | 24.13 |
| 15 | Gemini 3.5 Flash | 50 | 70 | 62.0 | 1,040.88 | 28.90 | 19.82 | 22.58 |
| 16 | Qwen3.7 Max | 46 | 66 | 58.0 | 1,631.35 | 17.43 | 11.83 | 21.72 |
| 17 | Kimi K2.7 Code | 42 | 61 | 53.4 | 524.56 | 64.33 | 33.87 | 18.36 |
| 18 | GPT-5.5 (high) | 53 | 72 | 64.4 | 1,654.59 | 30.98 | 12.95 | 17.96 |
| 19 | GPT-5.6 Sol (xhigh) | 58 | 78 | 70.0 | 1,542.52 | 49.71 | 15.10 | 15.96 |
| 20 | Claude Opus 4.8 (max) | 56 | 74 | 66.8 | 3,752.55 | 24.57 | 5.92 | 13.89 |
| 21 | GPT-5.6 Luna (max) | 51 | 71 | 63.0 | 870.30 | 102.41 | 24.08 | 13.33 |
| 22 | Kimi K2.6 | 44 | 62 | 54.8 | 851.63 | 118.14 | 21.41 | 10.91 |
| 23 | GPT-5.6 Terra (max) | 55 | 77 | 68.2 | 1,753.94 | 142.75 | 12.94 | 8.61 |
| 24 | GPT-5.5 (xhigh) | 55 | 75 | 67.0 | 2,630.04 | 107.19 | 8.48 | 7.97 |
| 25 | GPT-5.4 (xhigh) | 51 | 71 | 63.0 | 2,131.77 | 118.17 | 9.83 | 7.93 |
| 26 | GPT-5.6 Sol (max) | 59 | 77 | 69.8 | 2,824.18 | 201.46 | 8.22 | 5.84 |
| 27 | Claude Fable 5 (with fallback) | 60 | 76 | 69.6 | 5,630.52 | 167.86 | 4.11 | 4.52 |
| 28 | Claude Sonnet 5 (max) | 53 | 72 | 64.4 | 4,010.12 | 205.24 | 5.34 | 4.48 |

## Analysis

### Best balanced choices

- **GPT-5.6 Terra (medium) is the overall value leader.** Its quality score of 57.4 is not exceptional, but it combines the third-best cost rating with the fastest response time in the dataset (5.47 seconds). This moves it from third on cost alone to first after speed is included.
- **GPT-5.6 Luna (high) is the strongest close alternative.** It has slightly lower quality (56.2), is 14% more expensive, and is 24% slower than Terra (medium), producing a final rating of 82.13.
- **GPT-5.6 Terra (high) and GPT-5.6 Sol (low) form the next tier.** Sol (low) has better quality and cost efficiency, while Terra (high) is faster. Their final ratings—66.57 and 68.23—are close enough that workload priorities should decide between them.

### Best quality/value compromise

- **GPT-5.6 Sol (medium)** is the clearest compromise when quality matters more than maximizing the index. Its quality score is 67.2, only 2.8 points below the dataset leader, while it ranks fifth on the final value rating.
- **GPT-5.6 Sol (high)** raises quality to 68.6 and is relatively quick at 13.85 seconds, but its higher benchmark cost reduces its final rating to 37.66. It still jumps from 16th on cost-only value to 8th when speed is considered.
- **GPT-5.6 Sol (xhigh)** has the highest weighted quality score (70.0), but ranks only 19th on value because it costs 1,542.52 and takes 49.71 seconds. It is a quality-first selection, not a value-first selection.

### Why speed changes the ranking

- **DeepSeek V4 Pro (max)** falls from first on cost rating to 12th overall. Its benchmark cost is the lowest in the table, but its 84.06-second response time is more than 15 times Terra (medium)'s time.
- **MiniMax-M3** falls from second to sixth for the same reason, although its 27.27-second time is much less severe than DeepSeek's.
- **GPT-5.6 Sol (high)** gains eight positions, the largest positive rank movement. Claude Opus 4.8 and Qwen3.7 Max each gain six positions, but their high costs keep their absolute final ratings modest.
- Very slow variants are consistently penalized: GPT-5.6 Sol (max), Claude Fable 5, and Claude Sonnet 5 all take more than 167 seconds and occupy the bottom three positions in the final rating.

### Quality is not the same as value

The top four quality scores belong to GPT-5.6 Sol (xhigh), GPT-5.6 Sol (max), Claude Fable 5, and GPT-5.6 Sol (high). Only Sol (high) appears in the final value top 10. The rating therefore answers **“how much weighted capability is obtained per unit of cost and time?”**, not **“which model is most capable?”**

The median model in this dataset costs 860.77 and responds in 29.47 seconds. The leading value models generally beat both medians by a wide margin. This confirms that the final ranking is driven by genuinely inexpensive, fast configurations rather than by small differences in benchmark quality.

### Practical selection guide

| Priority | Recommended model | Reason |
|---|---|---|
| Maximum cost + speed value | GPT-5.6 Terra (medium) | Highest final rating and fastest response |
| Stronger quality while retaining high value | GPT-5.6 Sol (medium) | 67.2 quality and fifth overall value rank |
| Maximum measured quality | GPT-5.6 Sol (xhigh) | Highest quality score, but weak value rating |
| Lowest benchmark cost | DeepSeek V4 Pro (max) | Cost leader, if 84.06-second latency is acceptable |
| Fast, low-cost alternative | GPT-5.6 Luna (high) | Second overall value rating |

## Interpretation and caveats

- **Higher is better.** A score of 100 identifies the best value in this particular dataset; 50 means half of the leader's measured value under the formula.
- **Scores are relative.** Adding or removing a model can change every normalized score, although the ranking among unchanged rows will remain the same.
- **Equal cost/speed penalty is an assumption.** The square root gives cost and response time equal weight. If cost should matter more, use `G2^0.7*I2^0.3` instead of `SQRT(G2*I2)`; the exponents should sum to 1.
- **Do not mix column H into the recommended index.** Benchmark cost in G already represents cost for the evaluated workload. Combining G and H would likely count price twice.
- **Guard against invalid inputs.** All current G and I values are positive. If future rows can contain blanks or zeroes, wrap the row calculation with `IFERROR(...,"")`.
- **Minor source-data cleanup:** the first column is named `Column 9` and contains unexplained `x` flags; `Gemini 3.1 Pro Preview` has a blank family; and `Gemini 3.5 Flash` uses `Google4` as its family. These issues do not affect the formulas above.

## Suggested final column

Add one column named `Value Index (40I/60C, cost+speed)` and use the formula from section 3. Keep the cost-only formula only if a second diagnostic column is helpful.
