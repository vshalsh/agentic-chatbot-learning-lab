"""Interactive local CLI; one process represents one private chat session."""

from .agent import Agent


def main() -> None:
    agent = Agent()
    previous_response_id = None
    print("Agentic Chatbot Learning Lab. Type /reset or /quit.")
    while True:
        try:
            question = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if question == "/quit":
            break
        if question == "/reset":
            previous_response_id = None
            print("Conversation context reset.")
            continue
        if not question:
            continue
        try:
            turn = agent.respond(question, previous_response_id)
        except Exception as exc:
            print(f"assistant> Request failed: {exc}")
            continue
        previous_response_id = turn.response_id
        print(f"assistant> {turn.text}")
        print(
            f"[model={turn.model}; input={turn.input_tokens}; output={turn.output_tokens}; "
            f"cached_input={turn.cached_input_tokens}; tool_calls={turn.tool_calls}]"
        )


if __name__ == "__main__":
    main()
