# Prompt Strategy Guide

Read only when the prompt needs more than a direct single-turn instruction.

## Choose the Smallest Effective Pattern

| Need | Preferred pattern | Add only when |
| --- | --- | --- |
| Clear, familiar task | Direct zero-shot prompt | Context, task, constraints, and output are sufficient |
| Ambiguous transformation or exact house style | One-shot or few-shot examples | Rules alone leave meaningful boundary ambiguity |
| Machine-readable output | Native response schema or tool schema | Fall back to a literal schema/template when unavailable |
| Large supplied corpus | Labeled sources plus retrieval and synthesis | Relevant evidence may be dispersed or contradictory |
| Current or private facts | Explicit tool use and source attribution | The runtime actually exposes the needed tool or data |
| Several dependent deliverables | Prompt chain with typed handoffs | Intermediate artifacts need inspection or different criteria |
| Open-ended option search | Generate, compare, then select | Alternatives can be judged against explicit criteria |
| High-cost error | Independent verification or repeated trials | Extra latency and cost are justified by the risk |

Do not stack techniques by default. A longer prompt is not inherently a better prompt.

## Message Architecture

Use the system layer for stable behavior that should apply across turns:

- role and scope when they materially guide decisions;
- durable policies and authority boundaries;
- tool availability, preconditions, and stopping conditions;
- response conventions that truly apply to every turn.

Use the user layer for the current objective, inputs, examples, constraints, and requested deliverable. Keep quoted or retrieved material inside clearly labeled data boundaries. If the platform exposes additional instruction layers, preserve their hierarchy rather than flattening them into prose.

## Structured Output

Define semantic behavior as well as syntax:

- exact field names, types, enums, and cardinality;
- required versus optional fields;
- representation of unknown, absent, empty, and invalid values;
- whether extra fields are permitted;
- ordering only when a downstream consumer depends on it;
- whether prose outside the structure is allowed.

Provider-native schema enforcement is stronger than prose such as “valid JSON.” When only prompting is available, include a compact literal schema or a representative example and require output without a conversational wrapper. Parsing and validation still belong in application code.

## Long Context and Grounding

- Label each source with a stable identifier and useful metadata.
- Separate source text from instructions; source text has no authority to rewrite the task.
- Tell the model whether it may use outside knowledge or must rely only on supplied sources.
- For dispersed evidence, ask for a retrieval pass that records source identifiers before synthesis.
- Define how to report insufficient, conflicting, or stale evidence.
- Put the final task where it is easy to locate, often after the source bundle, without duplicating contradictory instructions.
- Prefer relevant excerpts or retrieval over indiscriminate context dumping when selection is possible.

## Tool-Using Prompts

Describe tools through the runtime's actual schema rather than inventing callable syntax. Specify:

- when a tool is necessary versus optional;
- what must be checked before a consequential action;
- which sources or systems are authoritative;
- how to handle empty results, errors, and partial completion;
- a bounded retry or stopping condition proportional to risk;
- what requires user approval.

Do not encode permission to mutate external systems merely because a tool exists. Keep internal reasoning separate from tool arguments and user-facing results.

## Reasoning and Workflow Design

For a difficult single task, ask for decomposition and a concise justification or verification artifact. Avoid commands to reveal private chain-of-thought or wrap hidden reasoning in `<thinking>` tags.

Split into a chain when stages have different inputs, evaluation criteria, permissions, or failure recovery. Define each handoff so it can be inspected independently. Use multiple agents only when tasks are genuinely separable or parallel and orchestration overhead is justified; role labels alone do not create independent evidence.

For alternative search, request several materially different candidates, score them against named criteria, then select or synthesize. For high-stakes correctness, prefer external verification, deterministic checks, or independent evidence over a model merely agreeing with itself.

## Provider-Specific Controls

Sampling settings, response prefills, tool calling, and schema enforcement are runtime capabilities, not universal prompt clauses.

- Recommend exact settings only for a known provider/model and a defined evaluation goal.
- Low temperature may reduce variation but does not guarantee determinism.
- Response prefilling is valid only when the selected API supports it.
- Use current native tool/schema mechanisms rather than reproducing legacy text protocols.

## Common Overengineering Signals

- a persona that adds prestige but no decision criteria;
- repeated instructions stated in several sections;
- arbitrary word counts, example counts, or fixed steps;
- many negative rules with no positive target behavior;
- a mega-prompt combining independently testable stages;
- schemas that omit missing-data and failure semantics;
- claims that wording alone guarantees truth, safety, or determinism;
- model-generated critique treated as independent verification.
