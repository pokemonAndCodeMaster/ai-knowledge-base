Title: Meta-Harness

Description: Meta-Harness automatically optimizes model harnesses — the code determining what to store, retrieve, and present to an LLM — surpassing hand-designed systems on text classification, math reasoning, and agentic coding.

Source: https://yoonholee.com/meta-harness/

---

[Demo](https://yoonholee.com/meta-harness/#demo)
[Approach](https://yoonholee.com/meta-harness/#method)
[Results](https://yoonholee.com/meta-harness/#results)
[Text Classification](https://yoonholee.com/meta-harness/#text-clf)
[Math Reasoning](https://yoonholee.com/meta-harness/#math)
[Agentic Coding](https://yoonholee.com/meta-harness/#agentic)

[Paper](https://arxiv.org/abs/2603.28052)
[Code](https://github.com/stanford-iris-lab/meta-harness-tbench2-artifact)

## TerminalBench-2: Harness Evolution
This is not the run that produced our final reported harness. It is an earlier, smaller search run that we find especially instructive for understanding what Meta-Harness does internally. We deliberately chose a hard 19-task subset where most agents struggle (note the low baseline scores), so that improvements from pure harness changes would be clearly visible. Starting from Terminus-KIRA (28.5%), the search reaches 46.5% by iteration 7.
Step through the iterations to see the proposer's reasoning. It performs counterfactual diagnosis across execution traces, identifies specific failure modes by reading raw logs through the filesystem, and proposes targeted fixes. Each proposal is grounded in concrete evidence from prior runs. Full-benchmark results on all 89 tasks are in the [Results](https://yoonholee.com/meta-harness/#results) section below. Click any dot or use arrow keys to inspect code changes.

## What Makes This Different
There are many methods for optimizing text and code with LLM feedback. The key difference is how much the optimizer gets to see. Most prior methods compress everything into a short summary, a scalar score, or a sliding window of recent candidates. That works for small problems, but harness engineering produces failures that are hard to diagnose without seeing the raw execution trace.
Meta-Harness takes a different approach: it gives the proposer a filesystem containing the full source code, scores, and execution traces of every prior candidate. The proposer is a coding agent (Claude Code) that reads what it needs via grep, cat, and other standard tools. In practice, this means up to 10M tokens of diagnostic context per step, vs. at most 26K for all prior methods we surveyed. The result is that the proposer can trace a failure back to the specific harness decision that caused it, rather than guessing from a score. See [the paper](https://arxiv.org/abs/2603.28052) for details.

```
grep
```


```
cat
```

Context available per optimization step. Mtok/iter = estimated context per evaluation in each paper's largest setting. Hover a row for details.

### Text Classification
We follow the online text classification setup of ACE: an LLM receives labeled examples one at a time, updates its memory, and is evaluated on a held-out test set. We search over harnesses using three datasets — LawBench (215 classes), Symptom2Disease (22 classes), and USPTO-50k (180 classes) — with GPT-OSS-120B as the model. We ran 20 evolution iterations with two candidates per iteration, producing 40 candidate harnesses. All test sets are held out until the final evaluation.
Test accuracy on three text classification benchmarks (GPT-OSS-120B). Ctx = average additional input context (thousands of characters).
We also directly compare Meta-Harness against two representative program-search methods, OpenEvolve and TTT-Discover (with PUCT selection), giving each the same proposer and evaluation budget. Meta-Harness matches their final accuracy with 10× fewer evaluations, and its final accuracy surpasses theirs by more than 10 points. We attribute this to the filesystem-based interface: both OpenEvolve and PUCT compress history into a fixed prompt format, discarding the execution traces that Meta-Harness uses for targeted diagnosis.

### Math Reasoning
We study retrieval-augmented math solving: a language model is given retrieved examples from a large corpus before attempting each problem. Meta-Harness searches over retrieval programs that can implement arbitrary filtering, branching, and formatting logic using corpus metadata and BM25 scores. The corpus contains ≥500K problems drawn from eight open-source datasets. We evolve a single retrieval harness on a 250-problem search set, then evaluate it on 200 held-out IMO-level problems. The same harness is then tested on five models unseen during search, directly measuring transfer.
Retrieval-augmented math reasoning on 200 IMO-level problems (pass@1, avg. over 3 samples). Absolute improvement over no retriever in parentheses. The discovered Meta-Harness retrieval strategy improves reasoning across all five held-out models, with a 4.7-point average gain.

### Agentic Coding (TerminalBench-2)
TerminalBench-2 evaluates LLM agents on 89 Dockerized tasks spanning code translation, distributed ML setup, systems programming, bioinformatics, and cryptanalysis, with binary pass/fail grading and 5 independent trials per task. These tasks are difficult because they require long-horizon, fully autonomous execution under complex dependencies, truncated terminal outputs, and substantial domain knowledge.
Meta-Harness evolves the full coding harness (system prompts, tool definitions, completion-checking logic, and context management). The proposer reads per-task execution traces (command logs, error messages, timeout behavior) to diagnose failure modes and propose targeted fixes. We initialize search from two strong open baselines, Terminus 2 and Terminus-KIRA.
Pass rate on TerminalBench-2. Results for others are from the official leaderboard. Meta-Harness ranks #2 among all Opus 4.6 agents and #1 among all Haiku 4.5 agents.

```
@inproceedings{lee2026metaharness, title={Meta-Harness: End-to-End Optimization of Model Harnesses}, author={Lee, Yoonho and Nair, Roshen and Zhang, Qizheng and Lee, Kangwook and Khattab, Omar and Finn, Chelsea}, booktitle={Preprint}, year={2026} }
```


```
@inproceedings{lee2026metaharness, title={Meta-Harness: End-to-End Optimization of Model Harnesses}, author={Lee, Yoonho and Nair, Roshen and Zhang, Qizheng and Lee, Kangwook and Khattab, Omar and Finn, Chelsea}, booktitle={Preprint}, year={2026} }
```

[Academic Project Page](https://github.com/eliahuhorwitz/Academic-project-page-template)
[Nerfies](https://nerfies.github.io)

