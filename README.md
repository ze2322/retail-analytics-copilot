# Retail Analytics Copilot

[![tests](https://github.com/ze2322/retail-analytics-copilot/actions/workflows/ci.yml/badge.svg)](https://github.com/ze2322/retail-analytics-copilot/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A hybrid question-answering agent for retail analytics. It answers a business
question by deciding, per question, whether the answer lives in the **prose
policy documents**, in the **transactional database**, or in both — then returns
the answer together with the SQL it ran and the document chunks it cited.

Built on the Northwind sample dataset (16,282 orders spanning 2012–2023).

---

## What it does

Ask *"How many days can unopened beverages be returned?"* and it retrieves the
returns policy document and answers `14`.

Ask *"What are the top 3 products by revenue of all time?"* and it runs SQL
against the order tables and answers with the rows — citing `Products`,
`Order Details` and `Orders` as its sources.

Every answer carries four things beyond the result itself: the SQL that produced
it, a confidence score, a short explanation, and the list of citations. That
makes the output auditable rather than a bare number from a black box.

---

## How it works

```text
                         ┌──────────────┐
  question  ───────────► │    router    │  rule-based: sql / rag / hybrid
                         └──────┬───────┘
                                │
              ┌─────────────────┴─────────────────┐
              ▼                                   ▼
      ┌───────────────┐                  ┌─────────────────┐
      │  TF-IDF       │  policy docs     │  SQL generation │
      │  Retriever    │ ───────────────► │  LLM ─► template│
      └───────┬───────┘                  └────────┬────────┘
              │                                   │
              │                          ┌────────▼────────┐
              │                          │   SQLiteTool    │
              │                          └────────┬────────┘
              └─────────────────┬─────────────────┘
                                ▼
                        ┌───────────────┐
                        │  synthesize   │  answer + sql + confidence + citations
                        └───────────────┘
```

The agent degrades gracefully at every step. If the LLM is unavailable or
generates SQL that fails, it falls back to vetted SQL templates. If those return
nothing, it falls back to answering from the retrieved documents. A question
never fails outright because one component is missing — which is also why the
test suite can run the whole pipeline in CI with no model server present.

| Component | File | Role |
|---|---|---|
| Router | `agent/dspy_signatures.py` | Classifies each question as `sql`, `rag` or `hybrid` |
| Retriever | `agent/rag/retrieval.py` | TF-IDF over paragraph chunks of the `docs/` policies |
| SQL tool | `agent/tools/sqlite_tool.py` | Executes queries, returns `(rows, error)` instead of raising |
| Orchestrator | `agent/graph_hybrid.py` | LLM SQL → template SQL → RAG fallback chain |
| Synthesizer | `agent/dspy_signatures.py` | Assembles answer, citations and confidence |

---

## Requirements

- Python 3.11 or newer
- About 200 MB of disk space for dependencies, plus the 24 MB database already in the repo
- Optional: [Ollama](https://ollama.com) with a local model, for LLM-generated SQL

The agent runs **without** Ollama. Only the LLM SQL-generation path needs it;
everything else works from the SQL templates and the retriever.

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/ze2322/retail-analytics-copilot.git
```

```bash
cd retail-analytics-copilot
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

On Windows:

```bash
venv\Scripts\activate
```

On Linux or macOS:

```bash
source venv/bin/activate
```

### 4. Install the dependencies

```bash
pip install -r requirements.txt
```

### 5. Confirm the installation

```bash
python -m unittest discover -s tests -v
```

All 12 tests should pass. If they do, the database, the retriever and the SQL
templates are all wired up correctly.

---

## Enabling the LLM path (optional)

Skip this section if you only want the template and retrieval paths.

### 1. Install Ollama

Download and install it from <https://ollama.com/download>.

### 2. Pull the model

```bash
ollama pull phi3.5:3.8b-mini-instruct-q4_K_M
```

### 3. Start the Ollama server

```bash
ollama serve
```

Leave this running in its own terminal. The agent picks the LLM path up
automatically on its next run.

---

## Usage

### Web interface

```bash
streamlit run app.py
```

Then open <http://localhost:8501>. The sidebar has sample questions to start from.

### Batch evaluation

Run a file of questions and write one JSON object per answer:

```bash
python run_agent_hybrid.py --batch sample_questions_hybrid_eval.jsonl --out outputs.jsonl
```

### Python API

```python
from agent.graph_hybrid import HybridAgent

agent = HybridAgent(use_llm=False)          # True to try LLM-generated SQL first
answer = agent.ask("What are the top 3 products by revenue of all time?", "str")

print(answer["final_answer"])   # the rows
print(answer["sql"])            # the query that produced them
print(answer["citations"])      # ['Products', 'Order Details', 'Orders']
print(answer["confidence"])     # 0.9
```

### Input format

Each line of a batch file is one JSON object:

```json
{"id": "q1", "question": "How many days can unopened beverages be returned?", "format_hint": "int"}
```

`format_hint` is either `"int"` (coerce the first column of the first row to an
integer) or `"str"` (return the rows as they are).

---

## Project layout

```text
retail-analytics-copilot/
├── agent/
│   ├── dspy_signatures.py    # Router, citation extraction, answer synthesis
│   ├── graph_hybrid.py       # HybridAgent — the orchestration chain
│   ├── rag/retrieval.py      # TF-IDF retriever over docs/
│   └── tools/sqlite_tool.py  # Safe SQLite execution
├── data/northwind.sqlite     # Retail dataset (16,282 orders, 2012–2023)
├── docs/                     # Policy and KPI documents the retriever indexes
├── tests/test_agent.py       # 12 tests, no LLM required
├── app.py                    # Streamlit interface
├── run_agent_hybrid.py       # Batch CLI
└── sample_questions_hybrid_eval.jsonl
```

---

## Known limitations

These are deliberate scope boundaries, not open defects:

- **The router is rule-based**, matching on keywords rather than a learned
  classifier. It is predictable and free to run, but a question phrased unusually
  can land on the wrong branch.
- **The SQL templates cover the seasonal and top-N questions** listed in the
  sample file. Anything outside that set depends on the LLM path.
- **The retriever uses TF-IDF**, not dense embeddings, so it matches on shared
  vocabulary rather than meaning.
- **The confidence score is a heuristic** derived from which sources contributed,
  not a calibrated probability.

---

## License

Released under the [MIT License](LICENSE).
