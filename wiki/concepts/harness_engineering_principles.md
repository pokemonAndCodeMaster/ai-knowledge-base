---
title: Harness Engineering Principles
type: concept
tags: [methodology, principles, openai, anthropic]
---

# Harness Engineering Principles

Derived from the methodology developed by OpenAI and the Claude Code team (Anthropic) for large-scale agentic software development.

## 1. Humans Steer, Agents Execute
The software engineer's primary job is to design the environment, specify intent, and build feedback loops, not to write individual lines of code.

## 2. Repository as the System of Record
If information is not in the repository (e.g., Slack, Docs, Tribal Knowledge), it does not exist to the agent. Ground the agent strictly in version-controlled files.

## 3. AGENTS.md as a Table of Contents
Project-level instructions (`AGENTS.md`) should act as a pointer to deeper sources of truth (specs, patterns, tests), avoiding a singular "encyclopedic" file that exhausts context windows.

## 4. Mechanical Architecture Enforcement
Replace human code reviews for architectural invariants with mechanical sensors: custom linters, structural tests, and CI checks that provide instant feedback to the agent.

## 5. Agent Legibility First
Code and patterns should be optimized for AI readability and comprehension, ensuring the model can navigate and modify the codebase with high success rates.

## 6. Fewer, High-Expressiveness Tools
Progressive disclosure (agents discover context layer-by-layer) and composable primitive tools outperform sprawling, narrow toolkits.

## 7. See Like an Agent
Audit the model's actual outputs and failures. Evolve the harness based on where the agent struggles, rather than assuming model capability will fix everything.

## 8. Corrections are Cheap, Waiting is Expensive
In a high-throughput environment, "fixing forward" via autonomous corrections is more efficient than blocking development on slow human merge gates.

## References
- [[awesome_harness_readme|Awesome Agent Harness Readme]]
- [[steering_loop|Steering Loop]]
- [[agent_harness|Agent Harness]]
