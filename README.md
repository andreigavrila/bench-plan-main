# LLM Planning Benchmarks

## Overview

This project is dedicated to evaluating and benchmarking state-of-the-art (SOTA) Large Language Models (LLMs) to determine their planning, reasoning, and problem-solving capabilities. 

To achieve this, I leverage the [planning_benchmark](https://github.com/bladnman/planning_benchmark) framework.

The main idea of this repo is running these models/harnesses with the same evaluator gpt-5.4-xhigh-codex to see how they compare to each other and how much information they retain/lose during task execution.

## Method

While this benchmark has multiple flaws, including the process of evaluation which is not deterministic and insufiiciently scripted, it is a good starting point for evaluating LLMs on planning tasks. 

For the first 8 runs, I ran the evaluator gpt-5.4-xhigh-codex on each model and also manually check a sub-set of requirements to validate the evaluator.  

I plan to extend both the evaluation and the benchmark itself to make it more comprehensive and reliable but I think it is already useful as it is.

## Scores

### Performance Rankings (by Score)

| Model                    | gpt5.4-xhigh-codex  | Size | Cost  | Tokens  |
| ------------------------ | ------------------- | ---- | ----- | ------- |
| gpt5.4-xhigh-opencode    |        97.0%        | 24kB | 0.79$ |  73,472 |
| grok4.3-reasoning-kilo   |        96.9%        | 18kB | 0.19$ |  37,900 |
| opus4.7-max-claude       |        94.4%        | 35kB |       |         |
| gpt5.5-high-codex        |        94.4%        | 30kB |       |         |
| opus4.6-xhigh-kilo       |        93.9%        | 41kB | 1.54$ |  55,896 |
| deepseekv4pro-kilo       |        93.4%        | 27kB | 0.12$ |  42,400 |
| gpt5.4-xhigh-kilo-geai   |        92.9%        | 26kB |       |  62,613 |
| gpt5.5-xhigh-codex       |        91.9%        | 27kB |       |         |
| opus4.6-max-claudecode   |        90.9%        | 35kB |       |         |
| qwen3.6maxpreview-kilo   |        90.9%        | 57kB | 0.16$ |  52,300 |
| sonnet4.6-antigravity    |        90.4%        | 26kB |       |         |
| kimik2.6-opencode        |        89.9%        | 25kB | 0.08$ |  40,833 |
| gpt5.4-xhigh-codex       |        89.9%        | 23kB |       |         |
| gpt5.5-medium-codex      |        89.9%        | 21kB |       |         |
| glm5.1-opencode          |        88.9%        | 19kB | 0.08$ |  51,019 |
| qwen3.6pro-opencode      |        87.4%        | 22kB | 0.08$ |  39,716 |
| glm5.1-claudecode        |        86.9%        | 30kB |       |         |
| deepseek3.2-kilo         |        86.6%        | 25kB | 0.11$ |  45,249 |
| qwen3.6pro-kilo          |        85.9%        | 19kB | 0.11$ |  59,594 |
| glm5.1-kilo              |        83.3%        | 49kB | 0.08$ |  46,328 |
| hy3-preview-kilo         |        83.3%        | 19kB |       |  38,600 |
| mistralsmall4-opencode   |        75.8%        | 16kB | 0.03$ |  38,078 |
| kimik2.5-coda            |        75.8%        | 23kB | 0.40$ | 528,000 |
| mimov2.5pro-opencode     |        74.6%        | 23kB | 0.12$ |  41,180 |
| minimax2.7-opencode      |        72.7%        | 12kB | 0.03$ |  33,705 |
| kimik2.5-opencode        |        70.7%        | 58kB | 0.15$ |  47,796 |
| minimax2.5-free-opencode |        59.6%        |  8kB |       |  32,668 |
| glm4.6-coda              |        51.0%        | 23kB | 0.26$ | 436,477 |
| gemini3.1pro-antigravity |        45.6%        |  7kB |       |         |
| gemini3flash-antigravity |        40.4%        |  7kB |       |         |
| nemotron3super-kilo      |        27.8%        |  2kB | 0.09$ |  58,000 |

*(Note: The table above contains raw, unaltered stats and therefore missing cost data for some models.)*

### Smart ROI Analysis (Using Inferred Costs)

To accurately calculate Return on Investment (ROI), I have inferred the cost-per-run for models missing price data by using the known `1.54$` Opus measure and mapping it to the current cost ratio (Opus: $10, Sonnet: $6, GPT-5.4: $5.63, Gemini 3.1 Pro: $4.5, Gemini Flash: $1.13). The calculated ratio multiplier is `1.54 / 10 = 0.154`.

**Inferred Costs:**
*   **opus4.7-max-claude**: `~$1.54` (10 * 0.154)
*   **opus4.6-max-claudecode**: `~$1.54` (10 * 0.154)
*   **sonnet4.6-antigravity**: `~$0.92` (6 * 0.154)
*   **gpt5.4-xhigh-codex**: `~$0.87` (5.63 * 0.154)
*   **gpt5.4-xhigh-kilo-geai**: `~$0.87` (5.63 * 0.154)
*   **gemini3.1pro-antigravity**: `~$0.69` (4.5 * 0.154)
*   **gemini3flash-antigravity**: `~$0.17` (1.13 * 0.154)

Models without known or inferred cost data, including `gpt5.5-codex-*` and `glm5.1-claudecode`, are omitted from the value rankings until a cost basis is available.

#### Smart ROI Index Formula
A naive `Score / Cost` formula is heavily flawed because LLM performance does not scale linearly (a 5% jump from 90%->95% is drastically harder than 60%->65%). To fix this, the following formula calculates a **Smart Value Index**:

```text
Smart Value Index = ( (Score_percentage)^4 / (Cost_in_USD + $0.05) ) * 100
```
**Why this formula?**
1. **Score ^ 4**: Exponentiating to the fourth power heavily compounds high test scores, correctly rewarding SOTA capability even if it comes at a higher cost. 
2. **+$0.05 Base Cost**: We add a fixed infrastructure/latency proxy overhead to the denominator, avoiding a division by zero that would otherwise grant "free" models an infinite ROI loop. 

#### Value Rankings

| Model                      | Score     | Inferred Cost | Smart Value Index |
| -------------------------- | --------- | ------------- | ----------------- |
| **kimik2.6-opencode**      | **89.9%** |     $0.08     |     502.5         |
| **glm5.1-opencode**        | **88.9%** |     $0.08     |     480.5         |
| **qwen3.6pro-opencode**    | **87.4%** |     $0.08     |     448.9         |
| **deepseekv4pro-kilo**     | **93.4%** |     $0.12     |     447.7         |
| mistralsmall4-opencode     | 75.8%     |     $0.03     |     412.7         |
| glm5.1-kilo                | 83.3%     |     $0.08     |     370.4         |
| **grok4.3-reasoning-kilo** | **96.9%** |     $0.19     |     367.4         |
| **deepseek3.2-kilo**       | **86.6%** |     $0.11     |     351.5         |
| minimax2.7-opencode        | 72.7%     |     $0.03     |     349.2         |
| **qwen3.6pro-kilo**        | **85.9%** |     $0.11     |     340.3         |
| **qwen3.6maxpreview-kilo** | **90.9%** |     $0.16     |     325.1         |
| minimax2.5-free-opencode   | 59.6%     |     $0.00     |     252.4         |
| mimov2.5pro-opencode       | 74.6%     |     $0.12     |     182.1         |
| kimik2.5-opencode          | 70.7%     |     $0.15     |     124.9         |
| **gpt5.4-xhigh-opencode**  | **97.0%** |     $0.79     |     105.4         |
| **gpt5.4-xhigh-kilo-geai** | **92.9%** |     $0.87     |     81.0          |
| kimik2.5-coda              | 75.8%     |     $0.40     |     73.4          |
| **gpt5.4-xhigh-codex**     | **89.9%** |     $0.87     |     71.0          |
| **sonnet4.6-antigravity**  | **90.4%** |     $0.92     |     68.8          |
| **opus4.7-max-claude**     | **94.4%** |     $1.54     |     49.9          |
| **opus4.6-xhigh-kilo**     | **93.9%** |     $1.54     |     48.9          |
| **opus4.6-max-claudecode** | **90.9%** |     $1.54     |     42.9          |
| glm4.6-coda                | 51.0%     |     $0.26     |     21.8          |
| gemini3flash-antigravity   | 40.4%     |     $0.17     |     12.1          |
| gemini3.1pro-antigravity   | 45.6%     |     $0.69     |     5.8           |
| nemotron3super-kilo        | 27.8%     |     $0.09     |     4.3           |

*(Note: The items in bold above are the models scoring above 85%.)*

#### How to Interpret This Index

The Smart Value Index is directly proportional. A model with an index of **400** mathematically provides **4 times more value** per dollar than a model with an index of **100**, according to this formula. 

Keep in mind that "value" in this context is highly opinionated: because we take the score to the **4th power**, the index is designed to heavily penalize cheap but incompetent models. It ensures that a 90% capable model is treated as exponentially superior to a 60% capable model, rather than just 1.5x better. Therefore, if Model A has an index of 400 and Model B has 100, Model A is delivering four times the amount of "SOTA capability bang-for-your-buck."
