# Caching and efficiency patterns

Caching is not one feature. Choose a cache based on what can safely be reused, how it becomes stale, and whose data it contains.

| Layer | What is reused | Starter status | Main risk |
| --- | --- | --- | --- |
| Provider prompt/KV cache | Computation for an identical eligible input prefix | Supported by the selected model; default behavior is provider-managed | Prefix changes, expiry, region/routing differences can cause misses |
| Retrieval-result cache | Deterministic search results for the exact query and corpus snapshot | Implemented in process with a bounded LRU | A cache shared across tenants could leak private results |
| Embedding cache | Vectors for identical document chunks | Not implemented | Stale vectors after model/chunking changes |
| Semantic response cache | A previous answer for a similar query | Not implemented; add only with strict gates | Similarity can hide changed permissions, time, or intent |
| Conversation state | Earlier turns/tool results | CLI uses `previous_response_id` | Retention, ownership, stale history, context growth |

## Provider prompt caching

The OpenAI prompt-caching guide says caching is enabled automatically for supported models. It reuses eligible matching input prefixes; it does not cache an answer or guarantee a hit. The threshold and retention details vary by model and can change. Check the [live prompt-caching guide](https://developers.openai.com/api/docs/guides/prompt-caching).

For this starter:

- Reuse the same `INSTRUCTIONS` and `TOOLS` definitions each turn.
- Append new user content instead of rewriting stable prior context.
- Keep timestamps, user-specific content, and changing retrieval results after the stable prefix when your request structure allows it.
- Inspect `cached_tokens` in usage metadata. A zero is a useful signal to investigate, not proof of a bug.
- Do not add model-specific cache controls until you check that model's current API documentation.

## Local retrieval cache

The sample caches exact normalized query results using a snapshot of Markdown filenames, contents, and SHA-256 digests as part of the key. Editing a knowledge file changes the snapshot and naturally produces a cache miss. The process-local LRU is bounded; restart clears it. It is safe for this one local sample corpus, not a multi-tenant production cache.

If you move it to Redis, include tenant, authorization scope, corpus version, retrieval algorithm version, and query in the key. Set a TTL, redact logs, and invalidate when permissions or content changes.

## Semantic answer cache: advanced exercise

Do not cache assistant answers just because two embeddings are close. Before returning a cached answer, require the same tenant, authorization scope, corpus version, model/prompt version, tool policy, and freshness window. Reject cache use for time-sensitive questions, personal data, actions, ambiguous queries, or low similarity margins. Keep the sources and timestamp with every cached answer and offer a bypass flag. Evaluate wrong-cache rate as a first-class quality metric.

## Other cost and latency controls

- Use retrieval to keep the prompt focused instead of sending entire repositories.
- Cap result count, excerpt size, tool rounds, output tokens, and retries.
- Summarize old dialogue with a versioned, inspectable summary and retain critical user decisions.
- Use a cheaper model for low-risk classification only after evaluation; route hard cases to a stronger model.
- Stream output for perceived latency, but do not let streaming bypass tool validation or approvals.
- Compare total cost and grounded answer quality, not token count alone.
