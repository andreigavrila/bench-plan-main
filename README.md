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

| Model                    | codex-gpt5.4-xhigh  |  Size  |  Cost   | 
| ------------------------ | ------------------- | ------ | ------- |
| kilo-opus4.6-xhigh       |        93.9%        |  41kB  |  1.54$  |
| antigravity-sonnet4.6    |        90.4%        |  26kB  |         |
| codex-gpt5.4-xhigh       |        89.9%        |  23kB  |         |
| opencode-glm5.1          |        88.9%        |  19kB  |  0.08$  |
| opencode-qwen3.6pro      |        87.4%        |  22kB  |  0.08$  |
| kilo-qwen3.6pro          |        85.9%        |  19kB  |  0.11$  |
| kilo-glm5.1              |        83.3%        |  49kB  |  0.08$  |
| opencode-mistralsmall4   |        75.8%        |  16kB  |  0.03$  |
| opencode-minimax2.7      |        72.7%        |  12kB  |  0.03$  |
| opencode-kimik2.5        |        70.7%        |  58kB  |  0.15$  |
| opencode-minimax2.5-free |        59.6%        |   8kB  |  0.00$  |
| antigravity-gemini3.1pro |        45.5%        |   7kB  |         |
| antigravity-gemini3flash |        40.4%        |   7kB  |         |