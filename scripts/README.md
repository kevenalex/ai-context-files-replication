# scripts

Scripts of the collection steps, of the sample selection, and of the sample-based reproductions. Run
them from the repository root, as modules (`python -m scripts.<path>`). The settings are at the top
of each script.

| Script | Step | Input | Output |
|---|---|---|---|
| `ranking/run_ranking.py` | Ranking and cut-off at the top 10,000, compared with the study's | `data/collection/seart/seart_24-08-2025.json` | `results/collection/ranking_reproduction/` |
| `ranking/ranking.py` | Ranking algorithm of the replication package of Mohsenimofidi et al. (unmodified) | — | — |
| `detect_ai_context_files/run_detect_context.py` | Detection of the five formats via the GitHub API | `data/collection/ranking/top10000_24-08-2025.csv` | `results/collection/detection_rerun/` |
| `download_ai_context_files.py` | Download of the content of the detected files | `data/collection/detection/detection_top10000_2026-05-07.csv` | `results/collection/context_files_redownload/` |
| `reproduce_collection_sample.py` | Detection and download redone on 100 repositories of the top 10,000, compared with the study's collection | `data/collection/detection/`, `data/collection/context_files/` | `results/collection/sample_reproduction/` |
| `reproduce_classification_sample.py` | RQ1 classification redone on a sample (30 random files or the 97 validation files) with Claude Code | `data/collection/context_files/`, prompt in `data/rq01/classifier/` | `results/rq01/sample_reproduction/` |
| `reproduce_evidence_sample.py` | RQ2 evidence tracing redone on 8 random repositories with Claude Code | `data/rq02/manual_annotation/`, prompt in `data/rq02/evidence/` | `results/rq02/sample_reproduction/` |
| `sample_manual_validation.py` | Sample size (Cochran) and selection of the 47 repositories | `data/rq02/rq02_frame_149.csv` | `data/rq02/rq02_sample_47.csv` |

Detection and download need `GITHUB_TOKEN` in the `.env` file at the root. The reproductions of the
classification and of the evidence tracing need Claude Code installed and authenticated.
