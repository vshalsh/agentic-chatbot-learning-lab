# Forking guide

## 1. Choose the first use case

Pick a read-only assistant for a narrow corpus: team onboarding notes, product FAQs, an internal runbook, or a project guide. Define who can ask questions, which files may be retrieved, and what counts as a supported answer.

## 2. Configure model and context

Set `OPENAI_MODEL` to a model available to your API account. Update `MODEL_CONTEXT_WINDOW_TOKENS` and output/reasoning reserves from its live documentation; model names and limits change. Keep `examples/model-profile.json` as a dated snapshot and record when you last verified it.

## 3. Replace the knowledge base

Add small Markdown files to `knowledge_base/`. Do not add credentials, personal information, or material your intended users should not see. The sample index includes all Markdown files in that folder, so add access filtering before importing private or multi-tenant data.

## 4. Run checks before extending tools

```bash
python -m unittest discover -s tests -v
```

Add evaluation cases for your domain, especially missing answers, conflicting sources, stale evidence, and injected instructions.

## 5. Upgrade retrieval deliberately

For larger corpora, replace lexical search with embeddings or a search service. Preserve source IDs, access controls, freshness, chunk boundaries, and citation metadata. Cache embeddings by content hash plus embedding-model version. Cache retrieval results by tenant and corpus version.

## 6. Add external actions last

Begin with read-only tools. Any write or external side effect needs application-side authorization, input validation, idempotency, audit logs, limits, and a review or approval flow that matches its impact. Never let a prompt alone grant permission.

## 7. Document the fork

Update the README with your purpose, setup, model limits, data sources, tools, caching policy, privacy boundary, tests, and deployment assumptions. Add a license if you redistribute the fork.
