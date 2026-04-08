---
title: Persistent Context (in Repo)
type: concept
tags: [methodology, grounding, context]
---

# Persistent Context in Repo

## Definition
The practice of storing high-fidelity project specifications, requirements, design decisions, and architectural guidelines directly within the code repository (e.g., in a `docs/` or `.context/` folder).

## Purpose
- **Grounding**: Providing AI agents with a "source of truth" that is always current with the code.
- **Feedback**: Agents can read the context to verify if their proposed changes align with project goals.
- **Traceability**: Changes in requirements are version-controlled alongside changes in code.

## Key Components
- **Implementation Plans**: Living documents of how a feature should be built.
- **ADRs (Architecture Decision Records)**: The "Why" behind the code.
- **Linting Rules**: Enforcing style and policy through code.

## Relation to the Harness
Persistent context acts as a **Feedforward Guide** in the [[agent_harness|Agent Harness]], setting the constraints and directions for the agent before it starts implementing.

## References
- [[aws_ai_dlc|AWS AI-DLC Source]]
