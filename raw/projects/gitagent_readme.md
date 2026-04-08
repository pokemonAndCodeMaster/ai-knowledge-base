Source: https://raw.githubusercontent.com/open-gitagent/gitagent/main/README.md

---

[` | Run an agent from a git repo or local directory |
| `gitagent install` | Resolve and install git-based dependencies |
| `gitagent audit` | Generate compliance audit report |
| `gitagent skills ` | Manage skills (`search`, `install`, `list`, `info`) |
| `gitagent lyzr ` | Manage Lyzr agents (`create`, `update`, `info`, `run`) |

## Compliance

gitagent has first-class support for financial regulatory compliance:

### FINRA
- **Rule 3110** — Supervision: human-in-the-loop, escalation triggers, kill switch
- **Rule 4511** — Recordkeeping: immutable audit logs, retention periods, SEC 17a-4 compliance
- **Rule 2210** — Communications: fair/balanced enforcement, no misleading statements
- **Reg Notice 24-09** — Existing rules apply to GenAI/LLMs

### Federal Reserve
- **SR 11-7** — Model Risk Management: validation cadence, ongoing monitoring, outcomes analysis
- **SR 23-4** — Third-Party Risk: vendor due diligence, SOC reports, subcontractor assessment

### SEC / CFPB
- **Reg S-P** — Customer privacy, PII handling
- **CFPB Circular 2022-03** — Explainable adverse action, Less Discriminatory Alternative search

### Segregation of Duties
- **Roles & Permissions** — Define maker, checker, executor, auditor roles with controlled permissions
- **Conflict Matrix** — Declare which role pairs cannot be held by the same agent
- **Handoff Workflows** — Require multi-agent participation for critical actions (credit decisions, regulatory filings)
- **Isolation** — Full state and credential segregation between roles
- **DUTIES.md** — Root-level policy + per-agent role declarations
- **Enforcement** — Strict (blocks deployment) or advisory (warnings only)

Inspired by [Salient AI](https://www.trysalient.com/)'s purpose-built agent architecture and the [FINOS AI Governance Framework](https://air-governance-framework.finos.org/mitigations/mi-22_multi-agent-isolation-and-segmentation.html).

Run `gitagent audit` for a full compliance checklist against your agent configuration.

## Adapters

Adapters are used by both `export` and `run`. Available adapters:

| Adapter | Description |
|---------|-------------|
| `system-prompt` | Concatenated system prompt (works with any LLM) |
| `claude-code` | Claude Code compatible CLAUDE.md |
| `openai` | OpenAI Agents SDK Python code |
| `crewai` | CrewAI YAML configuration |
| `lyzr` | Lyzr Studio agent |
| `github` | GitHub Actions agent |
| `git` | Git-native execution (run only) |
| `opencode` | OpenCode instructions + config |
| `gemini` | Google Gemini CLI (GEMINI.md + settings.json) |
| `openclaw` | OpenClaw format |
| `nanobot` | Nanobot format |
| `cursor` | Cursor `.cursor/rules/*.mdc` files |

```bash
# Export to system prompt
gitagent export --format system-prompt

# Run an agent directly
gitagent run ./my-agent --adapter lyzr
```

## Inheritance & Composition

```yaml
# Extend a parent agent
extends: https://github.com/org/base-agent.git

# Compose with dependencies
dependencies:
  - name: fact-checker
    source: https://github.com/org/fact-checker.git
    version: ^1.0.0
    mount: agents/fact-checker
```

## Examples

See the `examples/` directory:

- **`examples/minimal/`** — 2-file hello world (agent.yaml + SOUL.md)
- **`examples/standard/`** — Code review agent with skills, tools, and rules
- **`examples/full/`** — Production compliance agent with all directories, hooks, workflows, sub-agents, SOD with DUTIES.md, and regulatory artifacts
- **`examples/gitagent-helper/`** — Helper agent that assists with creating gitagent definitions
- **`examples/lyzr-agent/`** — Example Lyzr Studio integration

## Specification

Full specification at [`spec/SPECIFICATION.md`](spec/SPECIFICATION.md).

JSON Schemas for validation at `spec/schemas/`.

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=open-gitagent/gitagent&type=Date)](https://star-history.com/#open-gitagent/gitagent&Date)

## Built with gitagent?

If you've built an agent using gitagent, we'd love to hear about it! [Open a discussion](https://github.com/open-gitagent/gitagent/discussions) or add a `gitagent` topic to your repo.

## License

MIT](https://raw.githubusercontent.com/open-gitagent/gitagent/main/README.md)

