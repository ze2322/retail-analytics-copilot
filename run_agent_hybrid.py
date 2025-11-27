<<<<<<< HEAD
import json
import click
from agent.graph_hybrid import HybridAgent

@click.command()
@click.option("--batch", type=str, required=True)
@click.option("--out", type=str, required=True)
def main(batch, out):
    agent = HybridAgent()
    results = []

    with open(batch, "r") as f:
        questions = [json.loads(line) for line in f]

    for q in questions:
        ans = agent.ask(q["question"], q.get("format_hint", "str"))
        results.append({"id": q["id"], **ans})

    with open(out, "w") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")

if __name__ == "__main__":
    main()
=======
import json
from agent.graph_hybrid import HybridAgent
import click

@click.command()
@click.option("--batch", type=str, required=True)
@click.option("--out", type=str, required=True)
def main(batch, out):
    agent = HybridAgent()
    results = []

    with open(batch, "r") as f:
        questions = [json.loads(line) for line in f]

    for q in questions:
        ans = agent.ask(q["question"], q.get("format_hint", "str"))
        results.append({"id": q["id"], **ans})

    with open(out, "w") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")

if __name__ == "__main__":
    main()
>>>>>>> 8e017c34374abf24b249e7e3dbbfa14b453c5c75
