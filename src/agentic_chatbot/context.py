"""Simple, tokenizer-independent context-budget arithmetic."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ContextUsage:
    context_window_tokens: int
    input_tokens: int
    output_reserve_tokens: int
    reasoning_reserve_tokens: int = 0
    safety_margin_tokens: int = 0

    @property
    def total_planned_tokens(self) -> int:
        return (
            self.input_tokens
            + self.output_reserve_tokens
            + self.reasoning_reserve_tokens
            + self.safety_margin_tokens
        )

    @property
    def remaining_tokens(self) -> int:
        return self.context_window_tokens - self.total_planned_tokens

    @property
    def fits(self) -> bool:
        return self.remaining_tokens >= 0


def plan_context(
    *,
    context_window_tokens: int,
    stable_instructions_tokens: int,
    tool_schema_tokens: int,
    history_tokens: int,
    retrieved_context_tokens: int,
    current_turn_tokens: int,
    output_reserve_tokens: int,
    reasoning_reserve_tokens: int = 0,
    safety_margin_tokens: int = 0,
) -> ContextUsage:
    """Calculate planned usage from externally measured token counts."""
    parts = (
        context_window_tokens,
        stable_instructions_tokens,
        tool_schema_tokens,
        history_tokens,
        retrieved_context_tokens,
        current_turn_tokens,
        output_reserve_tokens,
        reasoning_reserve_tokens,
        safety_margin_tokens,
    )
    if any(value < 0 for value in parts):
        raise ValueError("Token counts cannot be negative")
    input_tokens = sum(parts[1:6])
    return ContextUsage(
        context_window_tokens=context_window_tokens,
        input_tokens=input_tokens,
        output_reserve_tokens=output_reserve_tokens,
        reasoning_reserve_tokens=reasoning_reserve_tokens,
        safety_margin_tokens=safety_margin_tokens,
    )
