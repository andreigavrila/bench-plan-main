# LLM Planning Benchmarks

## Overview

This project is dedicated to evaluating and benchmarking state-of-the-art (SOTA) Large Language Models (LLMs) to determine their planning, reasoning, and problem-solving capabilities. 

To achieve this, I leverage the [planning_benchmark](https://github.com/bladnman/planning_benchmark) framework.

The main idea of this repo is running these models/harnesses through a consistent evaluator setup to see how they compare to each other and how much information they retain/lose during task execution.

## Method

While this benchmark has multiple flaws, including the process of evaluation which is not deterministic and insufiiciently scripted, it is a good starting point for evaluating LLMs on planning tasks. 

For the first 8 runs, I ran the evaluator gpt-5.4-xhigh-codex on each model and also manually check a sub-set of requirements to validate the evaluator. Starting with the five Fable 5 runs, I switched the evaluator from gpt5.4-xhigh-codex to gpt5.5-high. I ran multiple comparison tests with both evaluators before switching to ensure the scores stayed consistent enough for the leaderboard to remain comparable.

The `gpt5.6-terra-xhigh-codex` row is integrated from `gpt5.6-terra-xhigh-codex/results/PLAN_EVAL.md`. It scored 98.0% overall, with 100.0% critical coverage and four narrow important-level partial gaps. The main table leaves its benchmark cost blank because no direct bench cost was captured; the ROI section infers a rough cost from the other-task comparison where `gpt5.4-xhigh` cost `$5.65` and `gpt5.6-terra-xhigh` cost `$2.13`.

I plan to extend both the evaluation and the benchmark itself to make it more comprehensive and reliable but I think it is already useful as it is.

## Scores

### Performance Rankings (by Score)

| Model                           | Score  | Evaluator            | Size | Cost  | Tokens  |
| ------------------------------- | ------ | -------------------- | ---- | ----- | ------- |
| fable5-max-claudecode           | 100.0% | gpt5.5-high          | 51kB |       |  94,400 |
| opus4.8-max-claudecode          | 99.5%  | gpt5.5-high          | 37kB |       |  95,700 |
| opus4.8-xhigh-claudecode        | 99.5%  | gpt5.5-high          | 33kB |       |  85,700 |
| fable5-high-claudecode          | 99.0%  | gpt5.5-high          | 34kB |       |  74,700 |
| opus4.8-high-claudecode         | 99.0%  | gpt5.5-high          | 37kB |       |  75,500 |
| fable5-extra-claudecode         | 98.5%  | gpt5.5-high          | 48kB |       |  83,100 |
| gpt5.6-terra-xhigh-codex        | 98.0%  | gpt5.5-high          | 25kB |       |         |
| fable5-medium-claudecode        | 97.5%  | gpt5.5-high          | 21kB |       |  67,000 |
| gpt5.4-xhigh-opencode           | 97.0%  | gpt5.4-xhigh-codex   | 24kB | 0.79$ |  73,472 |
| gpt5.5-xhigh-codex              | 97.0%  | gpt5.5-high          | 34kB |       |         |
| grok4.3-reasoning-kilo          | 96.9%  | gpt5.4-xhigh-codex   | 18kB | 0.19$ |  37,900 |
| glm5.2-xhigh-kilo               | 96.0%  | gpt5.4-xhigh-codex   | 47kB | 0.15$ |  55,620 |
| qwen3.7max-kilo                 | 94.9%  | gpt5.4-xhigh-codex   | 34kB | 0.22$ |  47,203 |
| qwen3.7plus-kilo                | 94.4%  | gpt5.4-xhigh-codex   | 29kB | 0.07$ |  44,200 |
| gemini3.5flash-high-antigravity | 94.4%  | gpt5.4-xhigh-codex   | 35kB |       |         |
| opus4.7-max-claude              | 94.4%  | gpt5.4-xhigh-codex   | 35kB |       |         |
| gpt5.5-high-codex               | 94.4%  | gpt5.4-xhigh-codex   | 30kB |       |         |
| opus4.6-xhigh-kilo              | 93.9%  | gpt5.4-xhigh-codex   | 41kB | 1.54$ |  55,896 |
| minimaxm3-opencode              | 93.9%  | gpt5.4-xhigh-codex   | 43kB | 0.05$ |  48,002 |
| sonnet5-high-claudecode         | 93.4%  | gpt5.5-high          | 36kB |       |  91,700 |
| fable5-low-claudecode           | 93.4%  | gpt5.5-high          | 13kB |       |  63,600 |
| deepseekv4pro-kilo              | 93.4%  | gpt5.4-xhigh-codex   | 27kB | 0.12$ |  42,400 |
| gpt5.4-xhigh-kilo-geai          | 92.9%  | gpt5.4-xhigh-codex   | 26kB |       |  62,613 |
| kimik2.7code-opencode           | 91.9%  | gpt5.4-xhigh-codex   | 31kB | 0.08$ |  44,130 |
| opus4.6-max-claudecode          | 90.9%  | gpt5.4-xhigh-codex   | 35kB |       |         |
| qwen3.6maxpreview-kilo          | 90.9%  | gpt5.4-xhigh-codex   | 57kB | 0.16$ |  52,300 |
| mistral-medium3.5-opencode      | 90.9%  | gpt5.4-xhigh-codex   | 55kB | 0.43$ |  95,336 |
| sonnet4.6-antigravity           | 90.4%  | gpt5.4-xhigh-codex   | 26kB |       |         |
| kimik2.6-opencode               | 89.9%  | gpt5.4-xhigh-codex   | 25kB | 0.08$ |  40,833 |
| gpt5.4-xhigh-codex              | 89.9%  | gpt5.4-xhigh-codex   | 23kB |       |         |
| gpt5.5-medium-codex             | 89.9%  | gpt5.4-xhigh-codex   | 21kB |       |         |
| glm5.1-opencode                 | 88.9%  | gpt5.4-xhigh-codex   | 19kB | 0.08$ |  51,019 |
| sonnet5-max-claudecode          | 88.4%  | gpt5.5-high          | 47kB |       | 134,900 |
| qwen3.6pro-opencode             | 87.4%  | gpt5.4-xhigh-codex   | 22kB | 0.08$ |  39,716 |
| glm5.1-claudecode               | 86.9%  | gpt5.4-xhigh-codex   | 30kB |       |         |
| deepseek3.2-kilo                | 86.6%  | gpt5.4-xhigh-codex   | 25kB | 0.11$ |  45,249 |
| qwen3.6pro-kilo                 | 85.9%  | gpt5.4-xhigh-codex   | 19kB | 0.11$ |  59,594 |
| glm5.1-kilo                     | 83.3%  | gpt5.4-xhigh-codex   | 49kB | 0.08$ |  46,328 |
| hy3-preview-kilo                | 83.3%  | gpt5.4-xhigh-codex   | 19kB |       |  38,600 |
| mistralsmall4-opencode          | 75.8%  | gpt5.4-xhigh-codex   | 16kB | 0.03$ |  38,078 |
| kimik2.5-coda                   | 75.8%  | gpt5.4-xhigh-codex   | 23kB | 0.40$ | 528,000 |
| mimov2.5pro-opencode            | 74.6%  | gpt5.4-xhigh-codex   | 23kB | 0.12$ |  41,180 |
| minimax2.7-opencode             | 72.7%  | gpt5.4-xhigh-codex   | 12kB | 0.03$ |  33,705 |
| kimik2.5-opencode               | 70.7%  | gpt5.4-xhigh-codex   | 58kB | 0.15$ |  47,796 |
| minimax2.5-free-opencode        | 59.6%  | gpt5.4-xhigh-codex   |  8kB |       |  32,668 |
| gemma3-31b-kilo                 | 56.1%  | gpt5.4-xhigh-codex   |  4kB | 0.07$ |  36,400 |
| glm4.6-coda                     | 51.0%  | gpt5.4-xhigh-codex   | 23kB | 0.26$ | 436,477 |
| gemini3.1pro-antigravity        | 45.6%  | gpt5.4-xhigh-codex   |  7kB |       |         |
| gemini3flash-antigravity        | 40.4%  | gpt5.4-xhigh-codex   |  7kB |       |         |
| nemotron3super-kilo             | 27.8%  | gpt5.4-xhigh-codex   |  2kB | 0.09$ |  58,000 |

*(Note: The table above contains raw run metadata and therefore missing cost data for some models; inferred costs are handled only in the ROI section below.)*

### Smart ROI Analysis (Using Inferred Costs)

To accurately calculate Return on Investment (ROI), I infer missing cost-per-run values from the measured `opus4.6-xhigh-kilo` run: `$1.54` for `55,896` tokens. I treat this as the Opus-family baseline and scale it by the current blended prices:

* **Fable 5**: `$7.70`
* **Opus 4.* family**: `$3.85`
* **Sonnet 5**: `$2.31`
* **GPT-5.5 Codex rows without token counts**: xhigh uses `0.875 * Opus 4.8 xhigh/extra inferred run cost` (~`$2.07` per run), high uses `0.70 * gpt5.5-xhigh-codex inferred run cost` (~`$1.45` per run), and medium uses `0.38 * gpt5.5-xhigh-codex inferred run cost` (~`$0.79` per run), based on DeepSWE v1.1 cost positioning
* **GPT-5.6 Terra**: `$2.17` blended per 1M tokens; the xhigh row uses an inferred benchmark cost of `~$0.30`, conservatively `$0.40` or less
* **GPT-5.4**: `$2.17`

When token counts are available, the formula is `tokens * 1.54 / 55,896 * family_blended / 3.85`. When token counts are missing, I use the family-level estimate `family_blended * 1.54 / 3.85`, except for GPT-5.5 Codex rows where I use the requested DeepSWE-based extrapolation: xhigh is 87.5% of the inferred Opus 4.8 xhigh/extra run cost, high is 70% of the inferred GPT-5.5 xhigh run cost, and medium is 38% of the inferred GPT-5.5 xhigh run cost. For GPT-5.6 Terra xhigh, I use the cross-task ratio `2.13 / 5.65` against this benchmark's `$0.79` `gpt5.4-xhigh-opencode` cost, which gives `~$0.30`; rounded conservatively, it should be `$0.40` or less.

**Inferred Costs:**
*   **opus4.7-max-claude**: `~$1.54` (3.85 * 1.54 / 3.85)
*   **opus4.6-max-claudecode**: `~$1.54` (3.85 * 1.54 / 3.85)
*   **opus4.8-max-claudecode**: `~$2.64` (95,700 tokens * 1.54 / 55,896 * 3.85 / 3.85)
*   **opus4.8-xhigh-claudecode**: `~$2.36` (85,700 tokens * 1.54 / 55,896 * 3.85 / 3.85)
*   **opus4.8-high-claudecode**: `~$2.08` (75,500 tokens * 1.54 / 55,896 * 3.85 / 3.85)
*   **gpt5.5-high-codex**: `~$1.45` (0.70 * inferred `gpt5.5-xhigh-codex` cost of `$2.07`, per DeepSWE v1.1 extrapolation)
*   **gpt5.5-xhigh-codex**: `~$2.07` (0.875 * inferred `opus4.8-xhigh-claudecode` cost of `$2.36`, per DeepSWE v1.1 extrapolation)
*   **gpt5.5-medium-codex**: `~$0.79` (0.38 * inferred `gpt5.5-xhigh-codex` cost of `$2.07`, per DeepSWE v1.1 extrapolation)
*   **gpt5.6-terra-xhigh-codex**: `~$0.30` inferred (`$0.79 * $2.13 / $5.65`; conservative ceiling `$0.40` or less)
*   **gpt5.4-xhigh-codex**: `~$0.87` (2.17 * 1.54 / 3.85)
*   **gpt5.4-xhigh-kilo-geai**: `~$0.97` (62,613 tokens * 1.54 / 55,896 * 2.17 / 3.85)
*   **fable5-max-claudecode**: `~$5.20` (94,400 tokens * 1.54 / 55,896 * 7.70 / 3.85)
*   **fable5-high-claudecode**: `~$4.12` (74,700 tokens * 1.54 / 55,896 * 7.70 / 3.85)
*   **fable5-extra-claudecode**: `~$4.58` (83,100 tokens * 1.54 / 55,896 * 7.70 / 3.85)
*   **fable5-medium-claudecode**: `~$3.69` (67,000 tokens * 1.54 / 55,896 * 7.70 / 3.85)
*   **fable5-low-claudecode**: `~$3.50` (63,600 tokens * 1.54 / 55,896 * 7.70 / 3.85)
*   **sonnet5-high-claudecode**: `~$1.52` (91,700 tokens * 1.54 / 55,896 * 2.31 / 3.85)
*   **sonnet5-max-claudecode**: `~$2.23` (134,900 tokens * 1.54 / 55,896 * 2.31 / 3.85)

Models without known or inferred cost data, including `sonnet4.6-antigravity`, `gemini3.5flash-high-antigravity`, `gemini3.1pro-antigravity`, `gemini3flash-antigravity`, and `glm5.1-claudecode`, are omitted from the value rankings until a cost basis is available.

#### Smart ROI Index Formula
A naive `Score / Cost` formula is heavily flawed because LLM performance does not scale linearly (a 5% jump from 90%->95% is drastically harder than 60%->65%). To fix this, the following formula calculates a **Smart Value Index**:

```text
Smart Value Index = ( (Score_percentage)^4 / (Cost_in_USD + $0.05) ) * 100
```
**Why this formula?**
1. **Score ^ 4**: Exponentiating to the fourth power heavily compounds high test scores, correctly rewarding SOTA capability even if it comes at a higher cost. 
2. **+$0.05 Base Cost**: We add a fixed infrastructure/latency proxy overhead to the denominator, avoiding a division by zero that would otherwise grant "free" models an infinite ROI loop. 

#### Recommended 95%+ Value Shortlist

This is the main decision table. It only includes the most useful models that clear the recommended capability tier.

**Best picks:**
* **Best value above 95%**: `glm5.2-xhigh-kilo`
* **Best cheap near-SOTA run**: `grok4.3-reasoning-kilo`
* **Best GPT-family value**: `gpt5.6-terra-xhigh-codex`
* **Best 99%+ value**: `opus4.8-high-claudecode`
* **Best absolute score**: `fable5-max-claudecode`

| Model                        | Score  | Est. Cost | Smart Value Index | Use When |
| ---------------------------- | ------ | ------------- | ----------------- | -------- |
| **glm5.2-xhigh-kilo**        | 96.0%  |     $0.15     |     424.7         | You want the best value above 95% |
| **grok4.3-reasoning-kilo**   | 96.9%  |     $0.19     |     367.4         | You want a very cheap near-SOTA run |
| **gpt5.6-terra-xhigh-codex** | 98.0%  |     $0.30     |     263.5         | You want the strongest GPT-family value row listed |
| **gpt5.4-xhigh-opencode**    | 97.0%  |     $0.79     |     105.4         | You want the measured GPT-5.4 baseline |
| **opus4.8-high-claudecode**  | 99.0%  |     $2.08     |     45.1          | You want the best 99%+ value |
| **gpt5.5-xhigh-codex**       | 97.0%  |     $2.07     |     41.7          | You want the strongest GPT-5.5 Codex option listed |
| **opus4.8-xhigh-claudecode** | 99.5%  |     $2.36     |     40.6          | You want the best 99.5% run |
| **fable5-medium-claudecode** | 97.5%  |     $3.69     |     24.2          | You want the best Fable value |
| **fable5-high-claudecode**   | 99.0%  |     $4.12     |     23.1          | You want a 99% Fable run |
| **fable5-max-claudecode**    | 100.0% |     $5.20     |     19.0          | You want the top score |

#### Full Value Rankings, Including 85%+ Models

The full table is the audit trail behind the shortlist. Models must score at least 85% to be listed here; below that cutoff, plans are usually incomplete enough that cost efficiency becomes misleading. Models highlighted in bold clear the 95% recommended tier.

| Model                        | Score      | Inferred Cost | Smart Value Index |
| ---------------------------- | ---------- | ------------- | ----------------- |
| minimaxm3-opencode           | 93.9%      |     $0.05     |     777.4         |
| qwen3.7plus-kilo             | 94.4%      |     $0.07     |     661.8         |
| kimik2.7code-opencode        | 91.9%      |     $0.08     |     548.7         |
| kimik2.6-opencode            | 89.9%      |     $0.08     |     502.5         |
| glm5.1-opencode              | 88.9%      |     $0.08     |     480.5         |
| qwen3.6pro-opencode          | 87.4%      |     $0.08     |     448.9         |
| deepseekv4pro-kilo           | 93.4%      |     $0.12     |     447.7         |
| **glm5.2-xhigh-kilo**        | **96.0%**  |     $0.15     |     424.7         |
| **grok4.3-reasoning-kilo**   | **96.9%**  |     $0.19     |     367.4         |
| deepseek3.2-kilo             | 86.6%      |     $0.11     |     351.5         |
| qwen3.6pro-kilo              | 85.9%      |     $0.11     |     340.3         |
| qwen3.6maxpreview-kilo       | 90.9%      |     $0.16     |     325.1         |
| **qwen3.7max-kilo**          | 94.9%      |     $0.22     |     300.4         |
| **gpt5.6-terra-xhigh-codex** | **98.0%**  |     $0.30     |     263.5         |
| mistral-medium3.5-opencode   | 90.9%      |     $0.43     |     142.2         |
| **gpt5.4-xhigh-opencode**    | **97.0%**  |     $0.79     |     105.4         |
| gpt5.5-medium-codex          | 89.9%      |     $0.79     |     77.8          |
| gpt5.4-xhigh-kilo-geai       | 92.9%      |     $0.97     |     73.0          |
| gpt5.4-xhigh-codex           | 89.9%      |     $0.87     |     71.0          |
| gpt5.5-high-codex            | 94.4%      |     $1.45     |     52.9          |
| opus4.7-max-claude           | 94.4%      |     $1.54     |     49.9          |
| opus4.6-xhigh-kilo           | 93.9%      |     $1.54     |     48.9          |
| sonnet5-high-claudecode      | 93.4%      |     $1.52     |     48.5          |
| **opus4.8-high-claudecode**  | **99.0%**  |     $2.08     |     45.1          |
| opus4.6-max-claudecode       | 90.9%      |     $1.54     |     42.9          |
| **gpt5.5-xhigh-codex**       | **97.0%**  |     $2.07     |     41.7          |
| **opus4.8-xhigh-claudecode** | **99.5%**  |     $2.36     |     40.6          |
| **opus4.8-max-claudecode**   | **99.5%**  |     $2.64     |     36.5          |
| sonnet5-max-claudecode       | 88.4%      |     $2.23     |     26.8          |
| **fable5-medium-claudecode** | **97.5%**  |     $3.69     |     24.2          |
| **fable5-high-claudecode**   | **99.0%**  |     $4.12     |     23.1          |
| fable5-low-claudecode        | 93.4%      |     $3.50     |     21.4          |
| **fable5-extra-claudecode**  | **98.5%**  |     $4.58     |     20.3          |
| **fable5-max-claudecode**    | **100.0%** |     $5.20     |     19.0          |

#### How to Interpret This Index

The Smart Value Index is directly proportional. A model with an index of **400** mathematically provides **4 times more value** per dollar than a model with an index of **100**, according to this formula. 

Keep in mind that "value" in this context is highly opinionated: because we take the score to the **4th power**, the index is designed to heavily penalize cheap but incompetent models. It ensures that a 90% capable model is treated as exponentially superior to a 60% capable model, rather than just 1.5x better. Therefore, if Model A has an index of 400 and Model B has 100, Model A is delivering four times the amount of "SOTA capability bang-for-your-buck."
