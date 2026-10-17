# Seven-lesson instructor plan

This sequence is designed for a hands-on learning lecture. Each session can run as a 45–75 minute workshop. Learners may use the sample code, then fork it for a project of their own.

## Lesson 1 — What model sees: context and budget

**Objective:** Explain the selected model, its available tools, context window, and the difference between maximum context and a safe request budget.

**Lecture:** Walk through `docs/model-context.md` and `examples/context-budget.json`. Count instructions, tool schema, history, evidence, current turn, output, reasoning, and margin. Discuss why “send the whole knowledge base” is not a context strategy.

**Exercise:** Change history and retrieved-token allocations. Determine when the request stops fitting and what should be trimmed first.

**Exit check:** Learner can state the selected model ID and find its live context limit in the provider's model documentation.

## Lesson 2 — From chatbot to agent

**Objective:** Trace a tool call end to end and identify the application as the authority that executes it.

**Lecture:** Read `docs/agent-loop.md`; trace `Agent.respond()` and `function_call_output`.

**Exercise:** Add a read-only date or calculator tool with a strict argument schema and a unit test.

**Exit check:** Learner can explain why a model-generated tool call is only a request.

## Lesson 3 — Grounded local retrieval

**Objective:** Retrieve evidence without loading the entire corpus into every prompt.

**Lecture:** Inspect `knowledge_base/` and the local lexical ranker. Explain top-k, excerpts, provenance, and the limitations of keyword search.

**Exercise:** Add two Markdown pages, ask comparative questions, and make answers cite source names.

**Exit check:** An unsupported answer is labeled unknown, not invented.

## Lesson 4 — Caching without stale answers

**Objective:** Distinguish prompt-prefix caching from deterministic retrieval caching and semantic answer caching.

**Lecture:** Read `docs/caching-and-efficiency.md`. Inspect cache hit metadata and clear the process-local cache.

**Exercise:** Run an identical search twice, edit the source, and confirm the content snapshot causes a miss. Propose tenant-aware keys for Redis.

**Exit check:** Learner can describe the invalidation rule for each cache layer.

## Lesson 5 — Tool safety and privacy

**Objective:** Constrain agent capabilities and defend against prompt injection in retrieved text.

**Lecture:** Read `docs/safety-and-evaluation.md`. Review allowlist, argument validation, read-only scope, and human approval requirements.

**Exercise:** Add a malicious instruction to a sample Markdown page; demonstrate it is quoted or ignored as data. Add a negative test.

**Exit check:** No model output is executed as code and no tool can exceed its application-side authorization.

## Lesson 6 — Evaluation and instrumentation

**Objective:** Evaluate whether the chatbot is useful and grounded, not merely fluent.

**Lecture:** Design a test set and metrics for groundedness, retrieval, citation correctness, latency, tokens, and cache behavior.

**Exercise:** Add one regression case for an answer absent from the corpus. Compare results before and after retrieval changes.

**Exit check:** A change that raises cache hits but harms evidence quality is rejected.

## Lesson 7 — Fork and adapt

**Objective:** Adapt the starter to a real project while preserving its safety and evidence boundaries.

**Lecture:** Follow `docs/forking-guide.md`; compare local documents with a database or vector index.

**Exercise:** Replace the sample corpus and model config; write down data flow, tenant boundary, freshness, and human approval needs.

**Exit check:** Fork contains setup instructions, current model limits, a working tool, tests, cache invalidation, and an explicit privacy statement.
