---
title: Mob Rituals (AI-DLC)
type: concept
tags: [methodology, coordination, collaboration]
---

# Mob Rituals

## Definition
Mob Rituals are collaborative ceremonies in the [[ai_dlc|AI-DLC]] where humans gather to steer, validate, and integrate AI agent outputs. They are the human "sensors" in the agent's feedback loop.

## The Two Primary Rituals

### 1. Mob Elaboration
- **Goal**: Validate the **Implementation Plan**.
- **Process**: Before an agent starts coding, humans (Engineers, PMs, Designers) review the agent's proposed plan for a [[bolts_and_work_units|Unit of Work]].
- **Outcome**: A refined, grounded plan that the agent can execute autonomously.

### 2. Mob Construction
- **Goal**: Steering during building.
- **Process**: Real-time collaborative sessions where humans guide an agent (or multiple agents) as they implement the code.
- **Role**: Humans provide the "steering" signals to the agent's [[steering_loop|Steering Loop]].

## Significance
Mob rituals solve the "Review Fatigue" problem. Instead of reviewing massive AI-generated PRs after the fact, humans review the **Intent and Plan** upfront, ensuring the output aligns with requirements from the start.

## References
- [[aws_ai_dlc|AWS AI-DLC Source]]
