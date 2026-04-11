# LLM Planning Benchmarks

## Overview

This project is dedicated to rigorously evaluating and benchmarking state-of-the-art (SOTA) Large Language Models (LLMs) to determine their planning, reasoning, and problem-solving capabilities. 

To achieve this, I leverage the [planning_benchmark](https://github.com/bladnman/planning_benchmark) framework. My core roadmap involves running these models through multiple independent test harnesses, ensuring a comprehensive and robust assessment across a diverse set of tasks.

## Objectives

- **Comprehensive Evaluation:** Assess the top tier of foundational models (e.g., GPT-5.4, Claude Opus 4.6, Gemini 3.1 Pro, Qwen 3.6 Pro, GLM 5.1, etc.) on complex planning scenarios.
- **Robust Methodology:** Utilize multiple distinct evaluation harnesses to prevent model overfitting to a specific test environment or prompt structure.
- **Actionable Insights:** Generate detailed metrics to highlight the strengths, vulnerabilities, and overall reliability of each model when tasked with autonomous, multi-step planning.

## Strategy

I integrate directly with the `planning_benchmark` repository to execute standardized tests. Each model under consideration is subjected to a tiered series of operational tasks designed to stress-test its long-horizon planning, context retention, and execution accuracy.

Scores and analytical data generated from these runs are tracked systematically in [**scores.txt**](./scores.txt) to provide transparent, easily comparable results across the AI ecosystem.
