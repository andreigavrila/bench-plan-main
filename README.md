# LLM Planning Benchmarks

## Overview

This project is dedicated to evaluating and benchmarking state-of-the-art (SOTA) Large Language Models (LLMs) to determine their planning, reasoning, and problem-solving capabilities. 

To achieve this, I leverage the [planning_benchmark](https://github.com/bladnman/planning_benchmark) framework.

The main idea of this repo is running these models/harnesses with the same evaluator codex-gpt-5.4-xhigh to see how they compare to each other and how much information they retain/lose during task execution.

## Method

While this benchmark has multiple flaws, including the process of evaluation which is not deterministic and insufiiciently scripted, it is a good starting point for evaluating LLMs on planning tasks. 

For the first 8 runs, I ran the evaluator codex-gpt-5.4-xhigh on each model and also manually check a sub-set of requirements to validate the evaluator.  

I plan to extend both the evaluation and the benchmark itself to make it more comprehensive and reliable but I think it is already useful as it is.

## Scores

### Performance Rankings (by Score)

| Model                    | codex-gpt5.4-xhigh  | Size | Cost  | Tokens  |
| ------------------------ | ------------------- | ---- | ----- | ------- |
| opencode-gpt5.4-xhigh    |        97.0%        | 24kB | 0.79$ |  73,472 |
| kilo-grok4.3-reasoning   |        96.9%        | 18kB | 0.19$ |  37,900 |
| claude-opus4.7-max       |        94.4%        | 35kB |       |         |
| codex-gpt5.5-high        |        94.4%        | 30kB |       |         |
| kilo-opus4.6-xhigh       |        93.9%        | 41kB | 1.54$ |  55,896 |
| kilo-geai-gpt5.4-xhigh   |        92.9%        | 26kB |       |  62,613 |
| codex-gpt5.5-xhigh       |        91.9%        | 27kB |       |         |
| claudecode-opus4.6-max   |        90.9%        | 35kB |       |         |
| antigravity-sonnet4.6    |        90.4%        | 26kB |       |         |
| opencode-kimik2.6        |        89.9%        | 25kB | 0.08$ |  40,833 |
| codex-gpt5.4-xhigh       |        89.9%        | 23kB |       |         |
| codex-gpt5.5-medium      |        89.9%        | 21kB |       |         |
| opencode-glm5.1          |        88.9%        | 19kB | 0.08$ |  51,019 |
| opencode-qwen3.6pro      |        87.4%        | 22kB | 0.08$ |  39,716 |
| claudecode-glm5.1        |        86.9%        | 30kB |       |         |
| kilo-deepseek3.2         |        86.6%        | 25kB | 0.11$ |  45,249 |
| kilo-qwen3.6pro          |        85.9%        | 19kB | 0.11$ |  59,594 |
| kilo-glm5.1              |        83.3%        | 49kB | 0.08$ |  46,328 |
| kilo-hy3-preview         |        83.3%        | 19kB |       |  38,600 |
| opencode-mistralsmall4   |        75.8%        | 16kB | 0.03$ |  38,078 |
| coda-kimik2.5            |        75.8%        | 23kB | 0.40$ | 528,000 |
| opencode-mimov2.5pro     |        74.6%        | 23kB | 0.12$ |  41,180 |
| opencode-minimax2.7      |        72.7%        | 12kB | 0.03$ |  33,705 |
| opencode-kimik2.5        |        70.7%        | 58kB | 0.15$ |  47,796 |
| opencode-minimax2.5-free |        59.6%        |  8kB |       |  32,668 |
| coda-glm4.6              |        51.0%        | 23kB | 0.26$ | 436,477 |
| antigravity-gemini3.1pro |        45.6%        |  7kB |       |         |
| antigravity-gemini3flash |        40.4%        |  7kB |       |         |

*(Note: The table above contains raw, unaltered stats and therefore missing cost data for some models.)*

### Smart ROI Analysis (Using Inferred Costs)

To accurately calculate Return on Investment (ROI), I have inferred the cost-per-run for models missing price data by using the known `1.54$` Opus measure and mapping it to the current cost ratio (Opus: $10, Sonnet: $6, GPT-5.4: $5.63, Gemini 3.1 Pro: $4.5, Gemini Flash: $1.13). The calculated ratio multiplier is `1.54 / 10 = 0.154`.

**Inferred Costs:**
*   **claude-opus4.7-max**: `~$1.54` (10 * 0.154)
*   **claudecode-opus4.6-max**: `~$1.54` (10 * 0.154)
*   **antigravity-sonnet4.6**: `~$0.92` (6 * 0.154)
*   **codex-gpt5.4-xhigh**: `~$0.87` (5.63 * 0.154)
*   **kilo-geai-gpt5.4-xhigh**: `~$0.87` (5.63 * 0.154)
*   **antigravity-gemini3.1pro**: `~$0.69` (4.5 * 0.154)
*   **antigravity-gemini3flash**: `~$0.17` (1.13 * 0.154)

Models without known or inferred cost data, including `codex-gpt5.5-*` and `claudecode-glm5.1`, are omitted from the value rankings until a cost basis is available.

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
| **opencode-kimik2.6**      | **89.9%** |     $0.08     |     502.5         |
| **opencode-glm5.1**        | **88.9%** |     $0.08     |     480.5         |
| **opencode-qwen3.6pro**    | **87.4%** |     $0.08     |     448.9         |
| opencode-mistralsmall4     | 75.8%     |     $0.03     |     412.7         |
| kilo-glm5.1                | 83.3%     |     $0.08     |     370.4         |
| **kilo-grok4.3-reasoning** | **96.9%** |     $0.19     |     367.4         |
| **kilo-deepseek3.2**       | **86.6%** |     $0.11     |     351.5         |
| opencode-minimax2.7        | 72.7%     |     $0.03     |     349.2         |
| **kilo-qwen3.6pro**        | **85.9%** |     $0.11     |     340.3         |
| opencode-minimax2.5-free   | 59.6%     |     $0.00     |     252.4         |
| opencode-mimov2.5pro       | 74.6%     |     $0.12     |     182.1         |
| opencode-kimik2.5          | 70.7%     |     $0.15     |     124.9         |
| **opencode-gpt5.4-xhigh**  | **97.0%** |     $0.79     |     105.4         |
| **kilo-geai-gpt5.4-xhigh** | **92.9%** |     $0.87     |     81.0          |
| coda-kimik2.5              | 75.8%     |     $0.40     |     73.4          |
| **codex-gpt5.4-xhigh**     | **89.9%** |     $0.87     |     71.0          |
| **antigravity-sonnet4.6**  | **90.4%** |     $0.92     |     68.8          |
| **claude-opus4.7-max**     | **94.4%** |     $1.54     |     49.9          |
| **kilo-opus4.6-xhigh**     | **93.9%** |     $1.54     |     48.9          |
| **claudecode-opus4.6-max** | **90.9%** |     $1.54     |     42.9          |
| coda-glm4.6                | 51.0%     |     $0.26     |     21.8          |
| antigravity-gemini3flash   | 40.4%     |     $0.17     |     12.1          |
| antigravity-gemini3.1pro   | 45.6%     |     $0.69     |     5.8           |

*(Note: The items in bold above are the models scoring above 85%.)*

#### How to Interpret This Index

The Smart Value Index is directly proportional. A model with an index of **400** mathematically provides **4 times more value** per dollar than a model with an index of **100**, according to this formula. 

Keep in mind that "value" in this context is highly opinionated: because we take the score to the **4th power**, the index is designed to heavily penalize cheap but incompetent models. It ensures that a 90% capable model is treated as exponentially superior to a 60% capable model, rather than just 1.5x better. Therefore, if Model A has an index of 400 and Model B has 100, Model A is delivering four times the amount of "SOTA capability bang-for-your-buck."
