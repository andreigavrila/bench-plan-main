# ðŸ“Š Model Benchmarking & Evaluation Results

> [!NOTE]
> This document summarizes the evaluation results of various language models. It details performance scores, evaluators, sizes, execution costs, generated tokens, and self-evaluation calibration statistics.

## ðŸ’¡ Key Highlights

* **ðŸ† Top Performers:** **fable5-max-claudecode** leads the benchmark at **100.0%**, followed by **opus4.8-max-claudecode** and **opus4.8-xhigh-claudecode** at **99.5%**, **fable5-high-claudecode** and **opus4.8-high-claudecode** at **99.0%**, and **fable5-extra-claudecode** at **98.5%**.
* **âš¡ Cost Efficiency:** **grok4.3-reasoning-kilo** achieves a near-top score of **96.9%** at a very low cost of **$0.19** (37,900 tokens), while **minimaxm3-opencode** reaches **93.9%** for **$0.05** (48,002 tokens) and **qwen3.7max-kilo** reaches **94.9%** for **$0.22** (47,203 tokens).
* **ðŸ“‰ Self-Evaluation Gap:** There is a significant calibration gap in some models. For example, **gemini3flash-antigravity** has a self-evaluation gap of **32%** (Self-Score of 72.22% vs Actual of 40.40%).

---

## ðŸ† Model Leaderboard

The table below lists the performance of all evaluated models, sorted in descending order of their scores. The score column is separated from the evaluator so mixed-evaluator runs can be tracked without renaming the table each time.

| Model                           | Score  | Evaluator          | Size |  Cost |  Tokens |
| ------------------------------- | :----: | ------------------ | ---: | ----: | ------: |
| fable5-max-claudecode           | 100.0% | gpt5.5-high        | 51kB |       |  94,400 |
| opus4.8-max-claudecode          | 99.5%  | gpt5.5-high        | 37kB |       |  95,700 |
| opus4.8-xhigh-claudecode        | 99.5%  | gpt5.5-high        | 33kB |       |  85,700 |
| fable5-high-claudecode          | 99.0%  | gpt5.5-high        | 34kB |       |  74,700 |
| opus4.8-high-claudecode         | 99.0%  | gpt5.5-high        | 37kB |       |  75,500 |
| fable5-extra-claudecode         | 98.5%  | gpt5.5-high        | 48kB |       |  83,100 |
| fable5-medium-claudecode        | 97.5%  | gpt5.5-high        | 21kB |       |  67,000 |
| gpt5.4-xhigh-opencode           | 97.0%  | gpt5.4-xhigh-codex | 24kB | 0.79$ |  73,472 |
| gpt5.5-xhigh-codex              | 97.0%  | gpt5.5-high        | 34kB |       |         |
| grok4.3-reasoning-kilo          | 96.9%  | gpt5.4-xhigh-codex | 18kB | 0.19$ |  37,900 |
| glm5.2-xhigh-kilo               | 96.0%  | gpt5.4-xhigh-codex | 47kB | 0.15$ |  55,620 |
| qwen3.7max-kilo                 | 94.9%  | gpt5.4-xhigh-codex | 34kB | 0.22$ |  47,203 |
| gemini3.5flash-high-antigravity | 94.4%  | gpt5.4-xhigh-codex | 35kB |       |         |
| opus4.7-max-claude              | 94.4%  | gpt5.4-xhigh-codex | 35kB |       |         |
| gpt5.5-high-codex               | 94.4%  | gpt5.4-xhigh-codex | 30kB |       |         |
| opus4.6-xhigh-kilo              | 93.9%  | gpt5.4-xhigh-codex | 41kB | 1.54$ |  55,896 |
| minimaxm3-opencode              | 93.9%  | gpt5.4-xhigh-codex | 43kB | 0.05$ |  48,002 |
| sonnet5-high-claudecode         | 93.4%  | gpt5.5-high        | 36kB |       |  91,700 |
| fable5-low-claudecode           | 93.4%  | gpt5.5-high        | 13kB |       |  63,600 |
| deepseekv4pro-kilo              | 93.4%  | gpt5.4-xhigh-codex | 27kB | 0.12$ |  42,400 |
| gpt5.4-xhigh-kilo-geai          | 92.9%  | gpt5.4-xhigh-codex | 26kB |       |  62,613 |
| opus4.6-max-claudecode          | 90.9%  | gpt5.4-xhigh-codex | 35kB |       |         |
| qwen3.6maxpreview-kilo          | 90.9%  | gpt5.4-xhigh-codex | 57kB | 0.16$ |  52,300 |
| sonnet4.6-antigravity           | 90.4%  | gpt5.4-xhigh-codex | 26kB |       |         |
| kimik2.6-opencode               | 89.9%  | gpt5.4-xhigh-codex | 25kB | 0.08$ |  40,833 |
| gpt5.4-xhigh-codex              | 89.9%  | gpt5.4-xhigh-codex | 23kB |       |         |
| gpt5.5-medium-codex             | 89.9%  | gpt5.4-xhigh-codex | 21kB |       |         |
| glm5.1-opencode                 | 88.9%  | gpt5.4-xhigh-codex | 19kB | 0.08$ |  51,019 |
| sonnet5-max-claudecode          | 88.4%  | gpt5.5-high        | 47kB |       | 134,900 |
| qwen3.6pro-opencode             | 87.4%  | gpt5.4-xhigh-codex | 22kB | 0.08$ |  39,716 |
| glm5.1-claudecode               | 86.9%  | gpt5.4-xhigh-codex | 30kB |       |         |
| deepseek3.2-kilo                | 86.6%  | gpt5.4-xhigh-codex | 25kB | 0.11$ |  45,249 |
| qwen3.6pro-kilo                 | 85.9%  | gpt5.4-xhigh-codex | 19kB | 0.11$ |  59,594 |
| glm5.1-kilo                     | 83.3%  | gpt5.4-xhigh-codex | 49kB | 0.08$ |  46,328 |
| hy3-preview-kilo                | 83.3%  | gpt5.4-xhigh-codex | 19kB |       |  38,600 |
| mistralsmall4-opencode          | 75.8%  | gpt5.4-xhigh-codex | 16kB | 0.03$ |  38,078 |
| kimik2.5-coda                   | 75.8%  | gpt5.4-xhigh-codex | 23kB | 0.40$ | 528,000 |
| mimov2.5pro-opencode            | 74.6%  | gpt5.4-xhigh-codex | 23kB | 0.12$ |  41,180 |
| minimax2.7-opencode             | 72.7%  | gpt5.4-xhigh-codex | 12kB | 0.03$ |  33,705 |
| kimik2.5-opencode               | 70.7%  | gpt5.4-xhigh-codex | 58kB | 0.15$ |  47,796 |
| minimax2.5-free-opencode        | 59.6%  | gpt5.4-xhigh-codex |  8kB |       |  32,668 |
| gemma3-31b-kilo                 | 56.1%  | gpt5.4-xhigh-codex |  4kB | 0.07$ |  36,400 |
| glm4.6-coda                     | 51.0%  | gpt5.4-xhigh-codex | 23kB | 0.26$ | 436,477 |
| gemini3.1pro-antigravity        | 45.6%  | gpt5.4-xhigh-codex |  7kB |       |         |
| gemini3flash-antigravity        | 40.4%  | gpt5.4-xhigh-codex |  7kB |       |         |
| nemotron3super-kilo             | 27.8%  | gpt5.4-xhigh-codex |  2kB | 0.09$ |  58,000 |

---

## ðŸ” Self-Evaluation Calibration

Self-evaluation calibration measures a model's ability to accurately assess its own performance. The **Gap** represents the difference between the model's self-score and its actual benchmark score (`Self-Score - Actual`). A smaller gap indicates better self-calibration.

| Model                    | Self-Score | Actual Score | Evaluator          | Gap  |
| ------------------------ | :--------: | :----------: | ------------------ | :--: |
| gpt5.4-xhigh-opencode    |   97.47%   |    96.97%    | gpt5.4-xhigh-codex | 0.5% |
| opus4.6-max-claudecode   |   97.0%    |    90.9%     | gpt5.4-xhigh-codex | 6.1% |
| opus4.7-max-claude       |   95.4%    |    94.4%     | gpt5.4-xhigh-codex |  1%  |
| geai-gpt5.4-xhigh-kilo   |   91.9%    |    92.9%     | gpt5.4-xhigh-codex | -1%  |
| glm5.1-claudecode        |   90.4%    |    86.9%     | gpt5.4-xhigh-codex | 3.5% |
| gemini3flash-antigravity |   72.22%   |    40.40%    | gpt5.4-xhigh-codex | 32%  |

---

## âš™ï¸ Metadata & References

* **ðŸ’¸ Total Evaluation Cost:** `~$0.8` (for the `OPENCODE-GPT5.4-xhigh EVAL` run)
* **ðŸ”— Leaderboard Reference:** [Artificial Analysis Coding Leaderboard](https://artificialanalysis.ai/models/capabilities/coding?models=gpt-5-4-mini%2Cgpt-5-4%2Cgpt-5-5%2Cclaude-sonnet-4-6-adaptive%2Cclaude-opus-4-7%2Cmistral-small-4%2Cdeepseek-v4-flash%2Cdeepseek-v4-pro%2Cminimax-m2-7%2Ckimi-k2-6%2Cmimo-v2-5-pro%2Cglm-5-1%2Cqwen3-6-plus%2Cclaude-opus-4-6-adaptive#coding-index)

