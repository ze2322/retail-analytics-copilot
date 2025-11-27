<<<<<<< HEAD
from typing import List, Dict, Optional
import re

# Rule-based router
def router(query: str) -> str:
    """Classify query into RAG, SQL, or Hybrid."""
    keywords_sql = ["top", "average", "sum", "revenue", "quantity", "aov", "margin"]
    q = query.lower()
    if any(k in q for k in keywords_sql):
        return "sql"
    elif "return" in q or "policy" in q:
        return "rag"
    else:
        return "hybrid"


def _extract_tables(sql: Optional[str]) -> List[str]:
    if not sql:
        return []
    candidates = ["Orders", "Order Details", "Products", "Customers", "Categories", "Suppliers"]
    found = []
    s = sql.lower()
    for t in candidates:
        if t.lower() in s:
            found.append(t)
    return found


def synthesize(final_result, doc_chunks: Optional[List[Dict]], sql_used: str, format_hint: str):
    doc_ids = []
    if doc_chunks:
        for c in doc_chunks:
            doc_ids.append(c.get("chunk_id") or c.get("id"))

    citations = []
    citations.extend(doc_ids)
    citations.extend(_extract_tables(sql_used))

    confidence = 0.5
    if sql_used:
        confidence += 0.3
    if doc_chunks:
        confidence += 0.1
    confidence = min(confidence, 0.99)

    return {
        "final_answer": final_result,
        "sql": sql_used,
        "confidence": round(confidence, 2),
        "explanation": "Derived from relevant documents and/or SQL query.",
        "citations": citations
    }
=======
from typing import List, Dict, Optional
import re


# Rule-based router
def router(query: str) -> str:
    """Classify query into RAG, SQL, or Hybrid."""
    keywords_sql = ["top", "average", "sum", "revenue", "quantity", "aov", "margin"]
    q = query.lower()
    if any(k in q for k in keywords_sql):
        return "sql"
    elif "return" in q or "policy" in q:
        return "rag"
    else:
        return "hybrid"


def _extract_tables(sql: Optional[str]) -> List[str]:
    if not sql:
        return []
    # simple detection from a whitelist of Northwind tables
    candidates = ["Orders", "Order Details", "Products", "Customers", "Categories", "Suppliers"]
    found = []
    s = sql.lower()
    for t in candidates:
        if t.lower() in s:
            found.append(t)
    return found


def synthesize(final_result, doc_chunks: Optional[List[Dict]], sql_used: str, format_hint: str):
    # Collect doc chunk ids (retriever returns 'chunk_id')
    doc_ids = []
    if doc_chunks:
        for c in doc_chunks:
            doc_ids.append(c.get("chunk_id") or c.get("id"))

    citations = []
    citations.extend(doc_ids)

    # Add DB table citations if SQL references them
    tables = _extract_tables(sql_used)
    citations.extend(tables)

    # Confidence heuristic
    confidence = 0.5
    if sql_used:
        confidence += 0.3
    if doc_chunks:
        confidence += 0.1
    confidence = min(confidence, 0.99)

    return {
        "final_answer": final_result,
        "sql": sql_used,
        "confidence": round(confidence, 2),
        "explanation": "Derived from relevant documents and/or SQL query.",
        "citations": citations
    }
>>>>>>> 8e017c34374abf24b249e7e3dbbfa14b453c5c75
