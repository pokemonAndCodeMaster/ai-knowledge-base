---
title: Conductor vs Orchestrator
type: concept
tags: [interaction-modes, methodology, management]
---

# Conductor vs Orchestrator

## Overview
Two distinct modes of human-agent interaction defined by Addy Osmani, representing the evolution from pair-coding to fleet management.

## Comparison

### Conductor
- **Scope**: Micro-level (Functions, single bugs).
- **Interaction**: Synchronous (real-time chat/edit).
- **Autonomy**: Low (agent waits for instructions).
- **Effort**: Concurrent (human active while AI works).
- **Metaphor**: A pairing session with a junior dev.

### Orchestrator
- **Scope**: Macro-level (Features, refactors, whole pipelines).
- **Interaction**: Asynchronous (delegate and check pull requests).
- **Autonomy**: High (agent plans and executes multi-step work).
- **Effort**: Front-loaded (specification) and Back-loaded (review).
- **Metaphor**: A Tech Lead managing a fleet of agents.

## Strategic Shift
The "Orchestrator" role represents the future of professional software engineering. Success depends on:
1. **Spec-Driven Development**: Writing unambiguous task descriptions.
2. **Reviewing Skills**: Treating PR review as a first-class citizen.
3. **System Design**: Defining how independent agent outputs mesh together.

## Relation to the Harness
- **Conductors** operate inside the [[steering_loop|Steering Loop]], providing real-time feedback.
- **Orchestrators** design the [[agent_harness|Harness]] itself, establishing the "tracks" (sensors, guides, environments) that allow many agents to run safely in parallel.

## References
- [[conductors_vs_orchestrators|Conductors to Orchestrators Source]]
