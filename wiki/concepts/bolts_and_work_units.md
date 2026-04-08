---
title: Bolts and Units of Work
type: concept
tags: [methodology, agile, ai-pace]
---

# Bolts and Units of Work

## Overview
New organizational primitives used in [[ai_dlc|AI-DLC]] to match the speed and granularity of AI agents.

## Units of Work (UoW)
- **Replaces**: Epics/User Stories.
- **Definition**: A strictly bounded, independent module or feature piece small enough for an AI agent to implement in a single pass.
- **Goal**: Atomicity. By keeping tasks small and decoupled, agents avoid the context-window drift found in complex stories.

## Bolts
- **Replaces**: Sprints.
- **Definition**: Short-duration, high-intensity work cycles (typically 1-2 days).
- **Process**:
    1. **Load**: Define UoWs for the Bolt.
    2. **Run**: Agents implement UoWs in parallel.
    3. **Land**: Humans review and merge agent PRs.
- **Inspiration**: The "Fast-Follow" philosophy.

## Why it matters
Traditional 2-week sprints are too slow for AI. Agents can finish a sprint's worth of code in hours. "Bolts" restructure the human feedback loop to maintain momentum without overwhelming the team.

## References
- [[aws_ai_dlc|AWS AI-DLC Source]]
