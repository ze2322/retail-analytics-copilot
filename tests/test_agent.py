"""End-to-end checks for the template and RAG paths.

These run without a local LLM: the agent is constructed with ``use_llm=False``
so the deterministic SQL templates and the TF-IDF retriever are exercised.
"""

import unittest

from agent.dspy_signatures import _extract_tables, router, synthesize
from agent.graph_hybrid import HybridAgent
from agent.rag.retrieval import Retriever
from agent.tools.sqlite_tool import SQLiteTool


class RouterTests(unittest.TestCase):
    def test_metric_questions_route_to_sql(self):
        for question in ("top 3 products by revenue", "average order value", "total quantity"):
            self.assertEqual(router(question), "sql")

    def test_policy_questions_route_to_rag(self):
        self.assertEqual(router("what is the return policy?"), "rag")

    def test_anything_else_falls_through_to_hybrid(self):
        self.assertEqual(router("who are our suppliers"), "hybrid")


class CitationTests(unittest.TestCase):
    def test_tables_are_extracted_from_sql(self):
        sql = 'SELECT * FROM Orders JOIN "Order Details" od ON o.OrderID = od.OrderID'
        self.assertIn("Orders", _extract_tables(sql))
        self.assertIn("Order Details", _extract_tables(sql))

    def test_no_sql_yields_no_table_citations(self):
        self.assertEqual(_extract_tables(None), [])

    def test_confidence_rises_when_sql_and_docs_are_both_present(self):
        docs = [{"chunk_id": "product_policy::chunk0", "content": "..."}]
        with_both = synthesize(1, docs, "SELECT 1 FROM Orders", "int")["confidence"]
        docs_only = synthesize(1, docs, "", "int")["confidence"]
        self.assertGreater(with_both, docs_only)


class SQLiteToolTests(unittest.TestCase):
    def test_valid_query_returns_rows(self):
        rows, err = SQLiteTool().run_query("SELECT COUNT(*) AS n FROM Orders")
        self.assertIsNone(err)
        self.assertGreater(rows[0]["n"], 0)

    def test_invalid_query_returns_an_error_instead_of_raising(self):
        rows, err = SQLiteTool().run_query("SELECT * FROM does_not_exist")
        self.assertIsNone(rows)
        self.assertIsNotNone(err)


class RetrieverTests(unittest.TestCase):
    def test_retriever_returns_scored_chunks(self):
        results = Retriever().retrieve("how long can beverages be returned")
        self.assertTrue(results)
        self.assertIn("chunk_id", results[0])
        self.assertGreaterEqual(results[0]["score"], 0.0)


class AgentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.agent = HybridAgent(use_llm=False)

    def test_policy_question_is_answered_from_the_documents(self):
        self.assertEqual(self.agent.ask(
            "How many days can unopened beverages be returned?", "int")["final_answer"], 14)

    def test_revenue_question_returns_rows_and_cites_the_tables(self):
        answer = self.agent.ask("What are the top 3 products by revenue of all time?", "str")
        self.assertEqual(len(answer["final_answer"]), 3)
        self.assertIn("Products", answer["citations"])
        self.assertIn("SELECT", answer["sql"])

    def test_seasonal_revenue_question_returns_a_non_empty_figure(self):
        answer = self.agent.ask("What was the total revenue for beverages during summer 2012?", "str")
        self.assertGreater(answer["final_answer"][0]["revenue"], 0)


if __name__ == "__main__":
    unittest.main()
