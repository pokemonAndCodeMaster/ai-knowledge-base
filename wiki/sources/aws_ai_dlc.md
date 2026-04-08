---
title: AWS AI-Driven Development Life Cycle (AI-DLC)
type: source
author: AWS (Dan McInerney, et al.)
url: https://aws.amazon.com/blogs/compute/ai-driven-development-life-cycle-ai-dlc/
tags: [aws, ai-dlc, methodology, rituals]
---

# AWS AI-Driven Development Life Cycle (AI-DLC)

## Overview
AWS defines AI-DLC as a fundamental shift in software engineering, moving from human-centric "Agile" to an **AI-centric** methodology. It addresses the "Pace Disparity" between AI's generation speed and human feedback loops.

## Key Rituals
- **Mob Elaboration**: The entire team (Product, Tech, QA) reviews and corrects AI-generated implementation plans *before* coding begins.
- **Mob Construction**: Collaborative, real-time guidance of the agent as it builds the solution, moving from "writing" to "steering."

## New Metaphors
- **Units of Work**: Replaces "Epics" with more granular, independent modules suited for AI.
- **Bolts**: Replaces "Sprints" with short (1-2 day), intense iterations focused on landing agent-built features.

## System Components
- **Persistent Context**: Storing specifications and requirements directly in the repo next to the code to ground the agent.
- **Automated Feedback Loops**: Comprehensive tests and linters acting as "sensors" for the agent.

## Related Concepts
- [[ai_dlc|AI-DLC]]
- [[mob_rituals|Mob Rituals]]
- [[bolts_and_work_units|Bolts and Work Units]]
- [[agent_harness|Agent Harness]]
