"""Sample-based reproduction of the RQ2 evidence tracing.

The evidence recorded in the manual annotation was split into atomic items, located in the files,
and mapped to an RQ1 category with Claude Code, using
`data/rq02/evidence/PROMPT_RQ02_EVIDENCE_TRACING_pt.md`. This script draws a sample of
repositories, builds an input with only those repositories, and runs the same prompt in
non-interactive mode. The comparison with the study's items is in
`notebooks/rq02/03_evidence_sample_reproduction.ipynb`.

Usage (from the repository root, with Claude Code installed and authenticated):
    python -m scripts.reproduce_evidence_sample
    python -m scripts.reproduce_evidence_sample --sample-only    # only builds the input
"""
import subprocess
import sys
from pathlib import Path

import pandas as pd

SAMPLE_SIZE = 8    # one batch of the prompt
SEED = 42
MODEL = "claude-sonnet-5-5"
LABELS = "data/rq02/manual_annotation/rq02_labels_annotator_A.csv"
PROMPT = "data/rq02/evidence/PROMPT_RQ02_EVIDENCE_TRACING_pt.md"
OUTPUT = "results/rq02/sample_reproduction"
MAX_SESSIONS = 5


def main():
    Path(OUTPUT).mkdir(parents=True, exist_ok=True)
    sample = pd.read_csv(LABELS).sample(SAMPLE_SIZE, random_state=SEED)
    sample_input = f"{OUTPUT}/input_sample.csv"
    sample.to_csv(sample_input, index=False)
    print(f"Sample of {len(sample)} repositories saved to {sample_input}")
    print(sample["repo"].to_string(index=False))

    # The prompt parameters keep the names of the original (Portuguese) prompt.
    message = (Path(PROMPT).read_text(encoding="utf-8")
               + f"\n\nENTRADA = {sample_input}\nPASTA_SAIDA = {OUTPUT}\n")
    if "--sample-only" in sys.argv:
        print(f"\nTo trace, send the prompt to Claude Code with ENTRADA = {sample_input} and PASTA_SAIDA = {OUTPUT}")
        return
    output = Path(f"{OUTPUT}/rq02_evidence.csv")
    for old in [output, Path(f"{OUTPUT}/rq02_evidence_items.csv")]:
        if old.exists():
            old.unlink()   # start over
    command = ["claude", "-p", "--model", MODEL,
               "--allowedTools", "Read", "Write", "Edit", "Bash(python3:*)", "Bash(python:*)",
               "Bash(mkdir:*)", "Bash(cat:*)", "Bash(ls:*)"]
    for session in range(1, MAX_SESSIONS + 1):
        done = len(pd.read_csv(output)) if output.exists() else 0
        if done >= len(sample):
            break
        print(f"\nSession {session}: {done}/{len(sample)} repositories. Tracing the next batch...")
        subprocess.run(command, input=message, text=True, check=True)
    print(f"Result in {OUTPUT}")


if __name__ == "__main__":
    main()
