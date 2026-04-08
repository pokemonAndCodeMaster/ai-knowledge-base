---
title: GitAgent Pattern (Repo-as-Agent)
type: concept
tags: [design-pattern, git, orchestration]
---

# GitAgent Pattern (Repo-as-Agent)

## Overview
The "GitAgent" pattern treats a version-controlled repository as the definitive definition of an AI agent. It moves agent configuration away from centralized platforms and into the codebase.

## Core Components
- **`agent.yaml`**: The manifest. Defines the agent's name, capabilities, dependencies, and model settings.
- **`SOUL.md`**: The identity. Defines the agent's persona, high-level objectives, and "reason for being."
- **`RULES.md`**: The constraints. Definitive boundaries on what the agent can and cannot do (Security, Style, Logic).
- **`DUTIES.md`**: Roles and permissions. Specifically for "Segregation of Duties" in multi-agent environments.

## Benefits
1. **Version Control**: Every change to an agent's persona or logic is tracked in Git.
2. **Infrastructure as Code**: Agents can be initialized, tested, and audited mechanically.
3. **Inheritance & Composition**: Agents can `extend` other repos, allowing for standardized "Base Agents" with specialized "Child Agents."
4. **Adapter Independence**: The same repo can be "exported" to different runtimes (Claude Code, OpenAI, etc.).

## Relation to Harness Engineering
The GitAgent pattern is a concrete implementation of [[harness_engineering_principles#2-repository-as-the-system-of-record|Principle #2: Repository as the System of Record]].

## References
- [[gitagent|GitAgent Source]]
