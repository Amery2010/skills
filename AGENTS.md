## Development policy

- Work in small, verifiable increments with clear acceptance criteria.
- Verify uncertain factual claims through web research before answering. If browsing is unavailable or inconclusive, state the uncertainty.

## Multi-agent orchestration

The primary agent owns planning, delegation, integration, final validation, and the final response.

Delegate only when it materially improves quality, speed, or context management. Handle trivial one-file edits and straightforward questions directly; avoid delegation when coordination costs outweigh the benefits.

Assign independent, bounded subtasks with clear scope, file ownership, and acceptance criteria. Use the least expensive available agent that can reliably complete each subtask:

- `luna_fast`: deterministic, read-only, low-risk work such as lookup, extraction, classification, and repetitive inspection.
- `luna_worker`: routine implementation, debugging, tests, localized refactoring, and integrations with clear acceptance criteria and limited impact.
- `sol_expert`: read-only analysis, architecture, diagnosis, and review for ambiguous or high-risk problems involving security, authorization, concurrency, migrations, performance, or cross-module behavior. Return evidence, tradeoffs, and an actionable implementation plan.
- `astra_worker`: exceptionally difficult implementation using `gpt-6-astra`. Use for changes requiring tightly coordinated behavior across modules, subtle correctness guarantees, complex algorithms, or difficult security, concurrency, and migration logic.

Route by the difficulty of the actual subtask, not its topic alone. Routine changes in a sensitive area do not automatically require Astra.

### Escalation and handoff

- Move from `luna_fast` to `luna_worker` when implementation or routine engineering judgment is needed.
- Use `sol_expert` when diagnosis, design, or risk analysis is the main challenge.
- Use `astra_worker` when implementation exceeds `luna_worker`'s reliable scope. Route directly when the difficulty is already clear; a prior failed attempt is not required.
- When Sol's analysis is needed first, pass its evidence, proposed approach, constraints, and acceptance criteria to the implementation agent.
- Do not require a Sol-to-Astra sequence for every difficult task.
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
