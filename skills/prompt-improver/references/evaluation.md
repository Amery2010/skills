# Prompt Evaluation

Read when the prompt will be reused, deployed, compared, or changed across model versions.

## Evaluate Behavior, Not Wording

Define acceptance criteria before comparing prompts. Prefer executable or observable checks over whether the output contains preferred headings or phrases.

A compact rubric can score each dimension from 0 to 2:

| Dimension | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Task success | Misses the objective | Partially useful | Completes the objective |
| Grounding | Unsupported or invented | Mixed support | Claims trace to allowed evidence |
| Constraint adherence | Breaks hard constraints | Minor misses | Meets required constraints |
| Output validity | Unusable or unparsable | Repairable | Valid for the consumer |
| Robustness | Fails ordinary variants | Handles common variants | Handles defined edge cases safely |
| Efficiency | Wasteful or looping | Acceptable | Proportionate cost and latency |

Weight dimensions according to the actual risk. A parser-facing prompt may weight output validity heavily; a research prompt may weight grounding and citation quality.

## Build a Small Representative Test Set

Include only cases that exercise meaningful behavior:

- a normal happy path;
- an underspecified input;
- a relevant edge or boundary case;
- conflicting or missing source data;
- untrusted input containing instruction-like text;
- unavailable tool or partial tool failure when tools are involved;
- malformed or empty data for structured-output workflows.

Add domain-specific safety or permission cases when consequential actions are possible. Do not create a huge synthetic suite before basic failures are understood.

## Compare Fairly

- Hold model, runtime configuration, tools, and test inputs constant when comparing prompt variants.
- Run enough repetitions to observe variance when sampling or model nondeterminism matters.
- Use deterministic validators for schemas, calculations, links, and other machine-checkable properties.
- Blind human or model-judge comparisons when subjective quality matters, and define the rubric before seeing results.
- Inspect failures, not just aggregate scores. A higher average must not hide a new critical regression.

Self-critique by the same model is a drafting aid, not independent evidence. Use external facts, validators, a separate evaluation pass, or human review when independence matters.

## Record the Prompt as a Versioned Artifact

For reusable production prompts, record:

- prompt ID, version, owner, purpose, and last review date;
- system and user layers separately;
- variables with types, required status, and trust level;
- expected model/runtime capabilities and tools;
- relevant generation settings without claiming determinism;
- evaluation set version, acceptance thresholds, and known limitations;
- rationale for material changes.

Keep prompt changes reviewable alongside the application behavior they affect. Re-run the representative evaluation set after prompt, model, tool, or schema changes.
