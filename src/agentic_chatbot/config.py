"""Environment-based settings; model limits are explicit and overrideable."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    model: str = "gpt-5.4-mini"
    context_window_tokens: int = 400_000
    output_reserve_tokens: int = 4_000
    reasoning_reserve_tokens: int = 8_000
    safety_margin_tokens: int = 8_000
    max_tool_rounds: int = 3
    knowledge_dir: str = "knowledge_base"

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            model=os.getenv("OPENAI_MODEL", cls.model),
            context_window_tokens=int(os.getenv("MODEL_CONTEXT_WINDOW_TOKENS", str(cls.context_window_tokens))),
            output_reserve_tokens=int(os.getenv("OUTPUT_RESERVE_TOKENS", str(cls.output_reserve_tokens))),
            reasoning_reserve_tokens=int(os.getenv("REASONING_RESERVE_TOKENS", str(cls.reasoning_reserve_tokens))),
            safety_margin_tokens=int(os.getenv("CONTEXT_SAFETY_MARGIN_TOKENS", str(cls.safety_margin_tokens))),
            max_tool_rounds=int(os.getenv("MAX_TOOL_ROUNDS", str(cls.max_tool_rounds))),
            knowledge_dir=os.getenv("KNOWLEDGE_DIR", cls.knowledge_dir),
        )

    @property
    def input_budget_tokens(self) -> int:
        return max(
            0,
            self.context_window_tokens
            - self.output_reserve_tokens
            - self.reasoning_reserve_tokens
            - self.safety_margin_tokens,
        )
