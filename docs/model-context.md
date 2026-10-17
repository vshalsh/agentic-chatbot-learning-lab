# Model and context: the complete request budget

**Reference profile checked 17 October 2026:** OpenAI API `gpt-5.4-mini`, called through the Responses API. The official model page lists a 400,000-token context window, a 128,000 maximum output, function calling support, and the `gpt-5.4-mini` alias plus a dated snapshot. See [the live model page](https://developers.openai.com/api/docs/models/gpt-5.4-mini). This profile is explicitly dated; model capabilities, availability, and limits change. Check the live page and the API account before using this configuration in a deployed product.

## What “full context” means

The model does not receive an abstract project or the entire chat UI. It receives the request the application constructs. That request can contain:

1. Stable developer instructions and safety rules.
2. Tool names, descriptions, and JSON parameter schemas.
3. Conversation history or a server-side conversation/response link.
4. The latest user message.
5. Retrieved documents, summaries, images, or other inputs.
6. Generated output and, for reasoning-enabled models, reasoning tokens.

The context window is the total budget, not a target prompt size. Inputs, output, and reasoning consume capacity. A long-running chat must retrieve selectively, summarize or compact when needed, and keep a reserve for the answer and tool loop. The [conversation-state guide](https://developers.openai.com/api/docs/guides/conversation-state) explains the context-window accounting and state options.

## Budget equation

```text
planned total = fixed instructions + tool schemas + history
              + retrieved evidence + current turn
              + output reserve + reasoning reserve + safety margin

request fits when planned total <= model context window
```

The `examples/context-budget.json` file provides one illustrative budget: 68,000 planned tokens of a 400,000-token window. These values are teaching examples; measure your real requests. The helper in `src/agentic_chatbot/context.py` does arithmetic from token counts supplied by the caller. It deliberately does not pretend character count is token count.

## Practical context policy

- Keep stable instructions concise, version-controlled, and first.
- Keep tool definitions small and unchanged across requests where possible.
- Retrieve only the top few relevant excerpts and cap excerpt length.
- Keep a rolling window of recent turns; summarize older turns with explicit uncertainty and preserved decisions.
- Reserve output capacity before assembling input. Tool loops consume additional requests.
- Log model ID, request ID, input/output tokens, cache-hit tokens, tool count, and latency; redact private content.
- Do not infer context capacity from a family name. Set the model ID and limits explicitly, then recheck at upgrade time.

## Configuration

`OPENAI_MODEL` selects the model. `MODEL_CONTEXT_WINDOW_TOKENS`, `OUTPUT_RESERVE_TOKENS`, `REASONING_RESERVE_TOKENS`, and `CONTEXT_SAFETY_MARGIN_TOKENS` make the working budget visible. The sample CLI displays usage returned by the API after each turn.

`previous_response_id` continues a conversation in this starter. It is a convenience for one CLI session, not an application database or tenant boundary. For durable products, store conversation-to-user ownership and retention metadata in your own authenticated store, and deliberately choose server-side versus client-side state. Chaining a response does not mean prior input is free; see the official state guide for current billing and retention behavior.
