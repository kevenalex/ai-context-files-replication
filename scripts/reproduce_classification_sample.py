"""Sample-based reproduction of the RQ1 classification by the LLM.

Classifying the 1,828 files takes several hours of Claude Code sessions. This script draws a sample
of files, builds a manifest with only those files, and runs the same prompt used in the study
(`data/rq01/classifier/PROMPT_RQ01_CLASSIFICATION_pt.md`) with Claude Code in non-interactive mode.
The comparison with the study's runs is in `notebooks/rq01/04_classifier_sample_reproduction.ipynb`.

Two samples are available:
- default: 30 files drawn among the 1,828 (seed 42), compared with the study's runs;
- `--validation`: the 97 files of the manual annotation, to recompute κ against the annotators' consensus.

Usage (from the repository root, with Claude Code installed and authenticated):
    python -m scripts.reproduce_classification_sample                  # random sample of 30
    python -m scripts.reproduce_classification_sample --validation     # the 97 validation files
    python -m scripts.reproduce_classification_sample --sample-only    # only builds the manifest
"""
import subprocess
import sys
from pathlib import Path

import pandas as pd

SAMPLE_SIZE = 30   # one batch of the prompt
SEED = 42
MODEL = "claude-sonnet-5-5"
MANIFEST = "data/collection/context_files/download_manifest.csv"
VALIDATION_SAMPLE = "data/rq01/manual_annotation/rq01_sample_files.csv"
MAX_SESSIONS = 10   # each Claude Code session classifies one batch of 30
PROMPT = "data/rq01/classifier/PROMPT_RQ01_CLASSIFICATION_pt.md"
OUTPUT = "results/rq01/sample_reproduction"


def main():
    validation = "--validation" in sys.argv
    run = "validation" if validation else "sample"
    Path(OUTPUT).mkdir(parents=True, exist_ok=True)
    man = pd.read_csv(MANIFEST, keep_default_na=False)
    man = man[man["status"] == "ok"]
    if validation:
        target = pd.read_csv(VALIDATION_SAMPLE)
        keys = set(target["repo"].str.lower() + "|" + target["arquivo"])
        sample = man[(man["repo"].str.lower() + "|" + man["file_label"]).isin(keys)]
    else:
        sample = man.sample(SAMPLE_SIZE, random_state=SEED)
    sample_manifest = f"{OUTPUT}/manifest_{run}.csv"
    sample.to_csv(sample_manifest, index=False)
    print(f"Sample of {len(sample)} files saved to {sample_manifest}")
    print(sample["file_label"].value_counts().to_string())

    # The prompt parameters keep the names of the original (Portuguese) prompt.
    message = (Path(PROMPT).read_text(encoding="utf-8")
               + f"\n\nEXECUCAO = {run}\nMANIFESTO = {sample_manifest}\nPASTA_SAIDA = {OUTPUT}\n")
    if "--sample-only" in sys.argv:
        print("\nTo classify, send the prompt to Claude Code with the parameters below, once per batch of 30:")
        print(f"  EXECUCAO = {run} | MANIFESTO = {sample_manifest} | PASTA_SAIDA = {OUTPUT}")
        return
    output = Path(f"{OUTPUT}/rq01_classification_run_{run}.csv")
    for old in [output, Path(f"{OUTPUT}/rq01_run_{run}_log.csv")]:
        if old.exists():
            old.unlink()   # start over
    command = ["claude", "-p", "--model", MODEL,
               "--allowedTools", "Read", "Write", "Edit", "Bash(python3:*)", "Bash(python:*)", "Bash(mkdir:*)"]
    for session in range(1, MAX_SESSIONS + 1):
        done = len(pd.read_csv(output)) if output.exists() else 0
        if done >= len(sample):
            break
        print(f"\nSession {session}: {done}/{len(sample)} classified. Classifying the next batch...")
        subprocess.run(command, input=message, text=True, check=True)
    print(f"Result in {output} ({len(pd.read_csv(output))} files)")


if __name__ == "__main__":
    main()
