# Agentic Chatbot Learning Lab

A practical, forkable course for building an agentic chatbot that knows when to answer, when to retrieve evidence, and how to manage model context and cost.

The starter uses the OpenAI Responses API with **GPT-5.4 Mini** as its documented reference model (400,000-token context window; verify current limits before deployment). It demonstrates a bounded, read-only knowledge search tool, a small local retrieval-result cache, conversation continuation, and provider prompt caching through stable prompt prefixes. The model name and token budgets are configurable.

> This is a teaching project, not a production-ready service. It runs as a local CLI and reads only Markdown files in `knowledge_base/`. It does not execute shell commands, send messages, or write to external systems.

## What you will learn

- How a tool-using chatbot differs from a prompt-only chatbot.
- What the selected model can do and how its context window is consumed.
- How to keep stable instructions and tool definitions cacheable while new turns are appended.
- When to use provider prompt caching, deterministic retrieval caching, or a semantic cache—and when not to cache.
- How to limit tool calls, preserve evidence, measure token usage, and evaluate quality.
- How to fork the starter and replace the sample knowledge base and tools safely.

## Quick start

Requirements: Python 3.11+ and an OpenAI API key with access to the selected model.

```bash
git clone https://github.com/vshalsh/agentic-chatbot-learning-lab.git
cd agentic-chatbot-learning-lab
python -m venv .venv
# Activate the virtual environment, then:
python -m pip install -e .
```

Set configuration in your shell. Do not commit secrets:

```bash
export OPENAI_API_KEY="your-api-key"
export OPENAI_MODEL="gpt-5.4-mini"
python -m agentic_chatbot
```

Try: `What does this lab teach about prompt caching?` Type `/reset` to begin a new conversation or `/quit` to exit.

## Learning sequence

| Lesson | Build or investigate | Checkpoint |
| --- | --- | --- |
| 1. Model and context | Read the model profile; budget input, reasoning, and output | Explain why a 400K window is not a 400K prompt budget |
| 2. Agent loop | Follow the request → tool call → tool result → final answer loop | Trace one `search_knowledge_base` call |
| 3. Grounded retrieval | Add and cite a small Markdown knowledge source | Verify every factual answer against a source excerpt |
| 4. Caching | Measure retrieval-cache hits and provider cached-token usage | Separate KV prompt caching from answer caching |
| 5. Safety | Add a tool and a policy test without granting broad authority | Demonstrate that the agent cannot call an unlisted tool |
| 6. Evaluation | Run the small offline tests and add regression cases | Measure groundedness, usefulness, latency, and tokens |
| 7. Fork and adapt | Replace the sample corpus and configure your own model | Document data boundaries and your chosen context budget |

See [the instructor-ready lesson plan](docs/lesson-plan.md) for objectives, lecture notes, exercises, and discussion prompts.

## Project map

- [`docs/model-context.md`](docs/model-context.md) — reference model facts and a practical context budget.
- [`docs/agent-loop.md`](docs/agent-loop.md) — tool execution flow and the limits of agent autonomy.
- [`docs/caching-and-efficiency.md`](docs/caching-and-efficiency.md) — provider prompt cache, retrieval cache, semantic cache, and trade-offs.
- [`docs/safety-and-evaluation.md`](docs/safety-and-evaluation.md) — security boundary and a small evaluation plan.
- [`docs/forking-guide.md`](docs/forking-guide.md) — adapt the example to another model, provider, or data source.
- [`examples/model-profile.json`](examples/model-profile.json) — dated configuration snapshot for the reference model.
- [`knowledge_base/`](knowledge_base/) — sample corpus searched by the local tool.

## Architecture

```text
User question
   ↓
Stable developer instructions + tool schema + conversation context
   ↓
GPT-5.4 Mini (Responses API)
   ├─ answer directly, or
   └─ call search_knowledge_base
          ↓
      bounded local Markdown search (exact-query cache)
          ↓
      source excerpts returned to the model
   ↓
Grounded response + request usage metadata
```

Prompt caching reuses eligible *input-prefix computation* when a later request matches; it does not cache a finished answer. The local retrieval cache saves repeated deterministic file-search work. These are distinct mechanisms.

## Run the offline checks

```bash
python -m unittest discover -s tests -v
```

Tests do not call the API and need no credentials.

## Day 1 scope

Day 1 establishes the name, audience, architecture, model profile, context budget, caching strategy, safety boundary, and seven-lesson teaching path. The next build days can expand the starter with telemetry, a web interface, a real embedding-backed index, and deployment guidance without changing the beginner-friendly foundation.

## License

MIT. See [`LICENSE`](LICENSE).
