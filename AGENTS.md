## Development policy

- Work in small, verifiable increments with clear acceptance criteria.
- Verify uncertain factual claims through web research before answering. If browsing is unavailable or inconclusive, state the uncertainty.

## Multi-agent orchestration

The primary agent owns planning, delegation, integration, final validation, and the final response. Handle routine implementation directly; delegate only when delegation materially improves quality, speed, or context management.

Assign independent, bounded subtasks with explicit file ownership and acceptance criteria. Choose the least expensive available agent that can reliably complete each subtask:

- `luna_fast`: deterministic, bounded, read-only support such as lookup, extraction, classification, formatting, and repetitive inspection.
- `sol_expert`: high-complexity, high-risk, or ambiguous analysis covering architecture, security, concurrency, migrations, performance, and other large-blast-radius decisions. Return evidence, tradeoffs, and an actionable implementation plan.
- `astra_worker`: exceptionally difficult implementation using `gpt-6-astra`, including tightly coupled behavior, complex algorithms, subtle correctness guarantees, and difficult security, concurrency, or migration logic.

Route by the actual difficulty of the subtask, not its topic alone. A sensitive topic does not automatically require `astra_worker`.

### Routing and handoff

- Use `luna_fast` for bounded fact-finding and read-heavy support; keep the implementation with the primary agent unless a harder implementation handoff is justified.
- Use `sol_expert` when diagnosis, design, or risk analysis is the main challenge.
- Use `astra_worker` directly when the implementation difficulty is already clear; do not manufacture an analysis handoff first.
- When analysis informs an implementation handoff, pass concrete evidence, constraints, and acceptance criteria to the implementation agent.
- Return conflicting conclusions, scope changes, and unresolved tradeoffs to the primary agent.

### Parallelism

- Parallelize independent read-only subtasks when delegation is worthwhile.
- Assign each file to at most one write-enabled agent at a time, including the primary agent.
- Serialize overlapping edits. Parallelize writes only when file ownership is clearly separated.
- Transfer file ownership explicitly during handoffs and preserve existing changes.
- Use at most 4 active subagents for ordinary tasks. Exceed this only for large-scale analysis with genuinely independent subtasks.

### Completion

Before reporting completion, the primary agent must:
1. Wait for all required subagents and review their evidence.
2. Resolve conflicts and integrate or adjust changes.
3. Perform project-level validation appropriate to the changes and within my permissions.
4. Briefly report which agents were used, why, and any validation limits.
