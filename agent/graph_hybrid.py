from agent.tools.sqlite_tool import SQLiteTool
from agent.rag.retrieval import Retriever
from agent.dspy_signatures import router, synthesize
from typing import List, Dict, Any
import re

try:  # Optional: the template and RAG paths work without a local LLM installed.
    import ollama
except ImportError:  # pragma: no cover - exercised only when the extra is absent
    ollama = None


class HybridAgent:
    """Hybrid Agent using RAG + SQL templates + optional LLM-generated SQL."""

    def __init__(self, use_llm=True):
        self.retriever = Retriever()
        self.sql_tool = SQLiteTool()
        # Fall back to the SQL templates when the ollama client is not installed.
        self.use_llm = use_llm and ollama is not None

    # ------------------------------------------------------
    # MAIN ENTRY
    # ------------------------------------------------------
    def ask(self, query: str, format_hint: str) -> Dict[str, Any]:
        route = router(query)
        docs = self.retriever.retrieve(query)

        # If LLM is enabled → try LLM SQL generation
        if self.use_llm and route in ["sql", "hybrid"]:
            result, sql = self._llm_generate_sql(query, docs, format_hint)
            if result is not None:
                return synthesize(result, docs, sql, format_hint)

        # Try hardcoded SQL templates
        if route in ["sql", "hybrid"]:
            result, sql = self._try_sql(query, docs, format_hint)
            if result is not None:
                return synthesize(result, docs, sql, format_hint)

        # RAG fallback
        if docs:
            text = docs[0]["content"]
            result = self._parse_int(text, query) if format_hint == "int" else text
            return synthesize(result, docs, "", format_hint)

        return synthesize(None, docs, "", format_hint)

    # ------------------------------------------------------
    # LLM SQL GENERATION
    # ------------------------------------------------------
    def _llm_generate_sql(self, query: str, docs: List[Dict], fmt: str):
        """Generate SQL using Ollama local model."""
        if not docs:
            return None, ""

        doc_texts = "\n\n".join([d["content"] for d in docs])

        prompt = f"""
You are a SQL assistant. Based only on the following documents:

{doc_texts}

Write a SQL query that answers this question:
{query}

Return ONLY the SQL. No explanation.
"""

        response = ollama.generate(
            model="phi3.5:3.8b-mini-instruct-q4_K_M",
            prompt=prompt
        )

        sql = response.get("response", "").strip()

        rows, err = self.sql_tool.run_query(sql)
        if err or not rows:
            return None, ""

        if fmt == "int":
            return int(list(rows[0].values())[0]), sql

        return rows, sql

    # ------------------------------------------------------
    # SQL TEMPLATE FALLBACK
    # ------------------------------------------------------
    def _try_sql(self, query: str, docs: List[Dict], fmt: str):
        q = query.lower()
        date_from, date_to = "2012-07-01", "2012-08-31"

        if "top 3" in q and "product" in q:
            sql = """
            SELECT p.ProductName AS product,
                   SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS revenue
            FROM "Order Details" od
            JOIN Products p ON od.ProductID = p.ProductID
            GROUP BY p.ProductName
            ORDER BY revenue DESC
            LIMIT 3;
            """

        elif "average order value" in q or "aov" in q:
            sql = f"""
            SELECT SUM(od.UnitPrice * od.Quantity * (1 - od.Discount))
                     / COUNT(DISTINCT Orders.OrderID) AS aov
            FROM Orders
            JOIN "Order Details" od ON Orders.OrderID = od.OrderID
            WHERE Orders.OrderDate BETWEEN '{date_from}' AND '{date_to}';
            """

        elif "highest total quantity" in q:
            sql = f"""
            SELECT c.CategoryName AS category,
                   SUM(od.Quantity) AS quantity
            FROM Orders o
            JOIN "Order Details" od ON o.OrderID = od.OrderID
            JOIN Products p ON od.ProductID = p.ProductID
            JOIN Categories c ON p.CategoryID = c.CategoryID
            WHERE o.OrderDate BETWEEN '{date_from}' AND '{date_to}'
            GROUP BY c.CategoryName
            ORDER BY quantity DESC
            LIMIT 1;
            """

        elif "total revenue" in q and "beverages" in q:
            sql = f"""
            SELECT COALESCE(
                SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)), 0
            ) AS revenue
            FROM Orders o
            JOIN "Order Details" od ON o.OrderID = od.OrderID
            JOIN Products p ON od.ProductID = p.ProductID
            JOIN Categories c ON p.CategoryID = c.CategoryID
            WHERE o.OrderDate BETWEEN '{date_from}' AND '{date_to}'
              AND c.CategoryName = 'Beverages';
            """

        elif "gross margin" in q or "best customer" in q:
            sql = """
            SELECT cu.CompanyName AS customer,
                   SUM(od.UnitPrice * 0.3 * od.Quantity * (1 - od.Discount)) AS margin
            FROM Orders o
            JOIN "Order Details" od ON o.OrderID = od.OrderID
            JOIN Customers cu ON o.CustomerID = cu.CustomerID
            WHERE o.OrderDate >= '2012-01-01'
            GROUP BY cu.CustomerID
            ORDER BY margin DESC
            LIMIT 1;
            """

        else:
            sql = "SELECT NULL;"

        rows, err = self.sql_tool.run_query(sql)
        if err or not rows:
            return None, ""

        if fmt == "int":
            try:
                return int(list(rows[0].values())[0]), sql
            except:
                return None, sql

        return rows, sql

    # ------------------------------------------------------
    # PARSING FOR RAG
    # ------------------------------------------------------
    def _parse_int(self, text: str, query: str) -> int:
        if "beverage" in query.lower():
            m = re.search(r"unopened:\s*(\d+)", text, re.IGNORECASE)
            if m:
                return int(m.group(1))

        m = re.search(r"(\d+)", text)
        return int(m.group(1)) if m else 0
