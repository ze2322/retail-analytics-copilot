# retail-analytics-copilot-
Hybrid AI agent for retail analytics using LangGraph, DSPy, and SQLite

# Retail Analytics Copilot

A hybrid AI agent for retail analytics using:
- **LangGraph** (≥6 nodes + repair loop)
- **DSPy Signatures** (Router, NL→SQL, Synthesizer)
- **TF-IDF/simple retriever**
- SQLite database integration
- Supports local LLM inference via Phi-3.5-mini-instruct

## Project Structure

```
retail-analytics-copilot/
├─ agent/
├─ data/
├─ docs/
├─ sample_questions_hybrid_eval.jsonl
├─ run_agent_hybrid.py
└─ requirements.txt
```

## How to Run
```bash
python run_agent_hybrid.py --batch sample_questions_hybrid_eval.jsonl --out outputs.jsonl
