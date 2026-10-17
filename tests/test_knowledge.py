import tempfile
import unittest
from pathlib import Path

from agentic_chatbot.knowledge import (
    clear_search_cache,
    search_cache_info,
    search_knowledge_base,
)


class KnowledgeSearchTests(unittest.TestCase):
    def setUp(self):
        clear_search_cache()
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "cache.md").write_text(
            "# Prompt cache\n\nStable prompt prefixes can be reused on a cache hit.\n",
            encoding="utf-8",
        )

    def tearDown(self):
        self.tmp.cleanup()
        clear_search_cache()

    def test_returns_evidence_filename_and_excerpt(self):
        result = search_knowledge_base("stable prompt prefix", str(self.root))
        self.assertEqual(result["results"][0]["source"], "cache.md")
        self.assertIn("cache hit", result["results"][0]["excerpt"])

    def test_exact_query_uses_cache_for_same_corpus_snapshot(self):
        search_knowledge_base("stable prompt prefix", str(self.root))
        search_knowledge_base("stable prompt prefix", str(self.root))
        info = search_cache_info()
        self.assertEqual(info.misses, 1)
        self.assertEqual(info.hits, 1)

    def test_corpus_edit_creates_a_new_cache_snapshot(self):
        search_knowledge_base("stable prompt prefix", str(self.root))
        (self.root / "cache.md").write_text("# Different\n\nNew retrieval text.\n", encoding="utf-8")
        result = search_knowledge_base("stable prompt prefix", str(self.root))
        self.assertEqual(result["results"], [])
        self.assertEqual(search_cache_info().misses, 2)


if __name__ == "__main__":
    unittest.main()
