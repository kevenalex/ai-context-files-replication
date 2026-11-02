#!/usr/bin/env python3
"""Stop hook: keeps Claude Code from ending its response while there are
pending files in the current run of the RQ1 classification.

It only acts when the session was started with CLASSIFICACAO_AUTO=<N> (the run number).
It lets the session stop if no new file was written since the last block,
to avoid an infinite loop.
"""
import csv, json, os, sys
from pathlib import Path

run = os.environ.get("CLASSIFICACAO_AUTO")
if not run:
    sys.exit(0)

root = Path(os.environ.get("CLAUDE_PROJECT_DIR", "."))
manifest = root / "data/collection/context_files/download_manifest.csv"
output = root / f"data/rq01/classifier/rq01_classification_run_{run}.csv"
state = root / f"data/rq01/classifier/.hook_state_run_{run}"

with open(manifest, newline="", encoding="utf-8") as f:
    target = {(r["repo"], r["file_label"]) for r in csv.DictReader(f) if r["status"] == "ok"}

done = set()
if output.exists():
    with open(output, newline="", encoding="utf-8") as f:
        done = {(r["repo"], r["arquivo_analisado"]) for r in csv.DictReader(f)}

n_done = len(target & done)
pending = len(target) - n_done
if pending == 0:
    sys.exit(0)

previous = int(state.read_text()) if state.exists() else -1
if n_done == previous:
    # No progress since the last block: let the session stop and report why.
    print(f"Classification stopped at {n_done}/{len(target)} with no progress since the last batch.", file=sys.stderr)
    sys.exit(0)
state.write_text(str(n_done))

# The instruction below goes to the model and is in Portuguese, like the prompt used in the study.
print(json.dumps({
    "decision": "block",
    "reason": (
        f"Execução {run}: {n_done}/{len(target)} classificados, {pending} pendentes. "
        "Releia a Parte A do prompt e classifique o próximo lote de 30 (B3 a B6). "
        "Não peça confirmação ao usuário."
    ),
}))
