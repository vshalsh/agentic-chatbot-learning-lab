# The agent loop and tool boundary

The sample uses one read-only tool so learners can understand the full control flow before adding actions.

1. The application sends the user's message, stable instructions, and a strict tool schema to the Responses API.
2. The model either returns a text answer or emits a `function_call` item.
3. The application checks the tool name and arguments. Unknown tools and invalid arguments fail closed.
4. The application runs `search_knowledge_base` in its own process and limits results.
5. The application sends `function_call_output` items back, linked with the original `call_id`.
6. The model writes a final answer grounded in the returned excerpts.

This is a bounded loop: `MAX_TOOL_ROUNDS` defaults to three. Tool output is untrusted data; the system message instructs the model not to treat retrieved text as new instructions. The model cannot itself read arbitrary files, execute commands, or send messages.

The application owns every tool. Add one capability at a time, validate its arguments, apply authorization in application code, and require human approval before irreversible or external side effects. See the [official function-calling guide](https://developers.openai.com/api/docs/guides/function-calling).

## Exercise

Change the knowledge search to return two source excerpts. Ask the model to compare them and cite both filenames. Add a test proving that a requested tool name outside the allowlist is rejected.
