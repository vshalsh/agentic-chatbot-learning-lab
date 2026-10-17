# Safety, privacy, and evaluation

## Starter safety boundary

- The only tool searches the local Markdown learning corpus.
- The tool is read-only, path-bounded, argument-validated, and limited to five excerpts.
- Tool names are allowlisted in application code. Model-generated tool arguments never become shell commands.
- Retrieved passages are treated as untrusted data and are never allowed to override developer instructions.
- The sample does not log prompts or retrieved excerpts. It prints high-level usage counts only.
- API keys belong in environment variables or a secret manager, never in source control.

Before adding a tool that writes, sends, purchases, deploys, or changes permissions, add identity checks, least privilege, idempotency, audit evidence, rate limits, and a human approval gate. Document the exact action boundary.

## Evaluation starter set

Create a small, versioned set of questions with expected source files and answer criteria:

1. Answer present in one file → should retrieve and cite the filename.
2. Answer spread across files → should retrieve multiple sources or disclose uncertainty.
3. Answer absent from corpus → should say it cannot establish the answer from local notes.
4. Prompt injection inside a Markdown file → should treat it as data and not follow it.
5. Empty or malformed tool arguments → should fail closed.
6. Unknown tool request → should not execute.
7. Long history → should preserve important facts and remain within the configured budget.

Score retrieval recall, groundedness, citation correctness, refusal/uncertainty quality, tool-call correctness, latency, input/output tokens, and cache-hit rate. Do not use cache-hit rate as a quality score.

## Privacy checklist for a fork

- Identify which input text leaves your machine and which files are sent to the model.
- Choose a conversation retention policy and state-store owner.
- Separate cache keys by tenant and authorization scope.
- Avoid putting secrets or personal data into prompts unless needed and approved.
- Keep audit logs useful without storing full prompt content by default.
- Recheck provider settings, region, retention, and model access for your deployment.
