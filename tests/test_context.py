import unittest

from agentic_chatbot.context import plan_context


class ContextBudgetTests(unittest.TestCase):
    def test_adds_all_request_components(self):
        usage = plan_context(
            context_window_tokens=100_000,
            stable_instructions_tokens=1_000,
            tool_schema_tokens=500,
            history_tokens=5_000,
            retrieved_context_tokens=2_000,
            current_turn_tokens=100,
            output_reserve_tokens=2_000,
            reasoning_reserve_tokens=1_000,
            safety_margin_tokens=1_000,
        )
        self.assertEqual(usage.input_tokens, 8_600)
        self.assertEqual(usage.remaining_tokens, 87_400)
        self.assertTrue(usage.fits)

    def test_flags_over_budget_request(self):
        usage = plan_context(
            context_window_tokens=10,
            stable_instructions_tokens=1,
            tool_schema_tokens=1,
            history_tokens=5,
            retrieved_context_tokens=1,
            current_turn_tokens=1,
            output_reserve_tokens=2,
        )
        self.assertFalse(usage.fits)

    def test_rejects_negative_counts(self):
        with self.assertRaises(ValueError):
            plan_context(
                context_window_tokens=10,
                stable_instructions_tokens=-1,
                tool_schema_tokens=0,
                history_tokens=0,
                retrieved_context_tokens=0,
                current_turn_tokens=0,
                output_reserve_tokens=0,
            )


if __name__ == "__main__":
    unittest.main()
