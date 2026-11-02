# AI Context Files in Practice: Adoption, Content, and Conflicts in Open-Source Repositories

Replication package of the paper. It contains the data, scripts, and notebooks that produce every
table, figure, and number in the paper, in the order in which the study was carried out.

## Research questions

- **RQ1**: How prevalent are AI context files in open-source repositories, and what categories of content do they contain?
- **RQ2**: How do AI context files that coexist in the same repository relate to each other?

## Structure

```
data/        input and intermediate data, by stage (collection/, rq01/, rq02/)
scripts/     collection: ranking, detection, download, and sample selection; sample-based reproductions
notebooks/   analyses: collection/, rq01/, rq02/
results/     tables and figures produced by the notebooks, by stage
docs/        historical record of the research process (overview-analise page)
```

Each folder has a `README.md` describing the content and origin of each file.

## Study workflow

| # | Step | How to reproduce | Output |
|---|---|---|---|
| 1 | Collection of repositories with SEART GitHub Search (2025-08-24) | input data (see `data/collection/README.md`) | `data/collection/seart/` |
| 2 | Ranking by popularity and maturity, and cut-off at the top 10,000 | `python -m scripts.ranking.run_ranking` | `data/collection/ranking/` |
| 3 | Detection of the five context file formats (2026-05-07) | `python -m scripts.detect_ai_context_files.run_detect_context` | `data/collection/detection/` |
| 4 | Download of the files' content (2026-06-24) | `python -m scripts.download_ai_context_files` | `data/collection/context_files/` |
| 5 | Adoption, formats, and download | `notebooks/collection/01_adoption_and_download.ipynb` | `results/collection/` |
| 6 | Sampling frame (487 → 149 repositories) | `notebooks/rq01/00_sampling_frame.ipynb` | `results/rq01/` |
| 7 | Selection of the sample of 47 repositories (97 files) | `python -m scripts.sample_manual_validation` | `data/rq02/rq02_sample_47.csv` |
| 8 | RQ1: manual annotation by the two annotators and consensus | input data | `data/rq01/manual_annotation/` |
| 9 | RQ1: LLM classification of the sample (validation, κ = 0.79) and of the 1,828 files (three runs) | procedure in `data/rq01/README.md` | `data/rq01/classifier/` |
| 10 | RQ1: agreement (κ) and classifier stability (agreement across runs) | `notebooks/rq01/01_sample_and_agreement.ipynb` | `results/rq01/` |
| 11 | RQ1: content of the files | `notebooks/rq01/02_content.ipynb` | `results/rq01/` |
| 12 | RQ1: differences across formats | `notebooks/rq01/03_formats.ipynb` | `results/rq01/` |
| 12a | RQ1: sample-based reproduction of the classification (optional) | `scripts/reproduce_classification_sample.py` and `notebooks/rq01/04_classifier_sample_reproduction.ipynb` | `results/rq01/sample_reproduction/` |
| 13 | RQ2: manual annotation by the two annotators and evidence | input data | `data/rq02/` |
| 14 | RQ2: agreement and prevalence of the relationships | `notebooks/rq02/01_agreement_and_relationships.ipynb` | `results/rq02/` |
| 15 | RQ2: evidence by category and conflict types | `notebooks/rq02/02_evidence_and_conflicts.ipynb` | `results/rq02/` |
| 15a | RQ2: sample-based reproduction of the evidence tracing (optional) | `scripts/reproduce_evidence_sample.py` and `notebooks/rq02/03_evidence_sample_reproduction.ipynb` | `results/rq02/sample_reproduction/` |

Steps 2 to 4 query GitHub and do not need to be redone: the outputs used in the paper are in
`data/`. To check the analyses, it is enough to run the notebooks (steps 5, 6, 10 to 12, 14, and 15).

## Where each result of the paper comes from

| In the paper | Notebook | File in `results/` |
|---|---|---|
| Data Collection: 228,890 SEART repositories, 1,256 with a file, 1,858 files, 1,828 downloaded | `collection/01_adoption_and_download` | — |
| Motivating example (dotCMS) | `collection/01_adoption_and_download` | — |
| Threats to Validity: 83 archived in the top 10,000, 62.4% overlap with Mohsenimofidi et al. | `collection/01_adoption_and_download` | — |
| Table of formats | `collection/01_adoption_and_download` | `collection/formats-table.svg` |
| Annotation Procedure: P35, frame of 149, sample of 47 | `rq01/00_sampling_frame`, `rq01/01_sample_and_agreement` | `rq01/pair_similarity.csv` |
| κ between annotators (RQ1) and κ of the classifier validation on the sample | `rq01/01_sample_and_agreement` | `rq01/classifier_validation_kappa.csv` |
| Stability across the three runs | `rq01/01_sample_and_agreement` | `rq01/run_stability.csv` |
| Table of categories | `rq01/02_content` | `rq01/categories-table.svg` |
| Co-occurrence figure (Jaccard) | `rq01/02_content` | `rq01/jaccard-categories-column.svg` |
| Figure of size by number of categories | `rq01/02_content` | `rq01/size-by-categories.svg` |
| Format × category table | `rq01/03_formats` | `rq01/format-category-single-file.svg` |
| κ between annotators (RQ2) and sample composition | `rq02/01_agreement_and_relationships` | — |
| Table of relationships (90% CI) | `rq02/01_agreement_and_relationships` | `rq02/relationship_prevalence.csv` |
| Repositories without redundancy and files that refer to another | `rq02/01_agreement_and_relationships` | `rq02/references_between_files.csv` |
| Figure of evidence by category | `rq02/02_evidence_and_conflicts` | `rq02/category-by-relationship.pdf` |
| Table of conflict types | `rq02/02_evidence_and_conflicts` | `rq02/conflict_types.csv` |

## How to reproduce

Requirements: Python 3.14 and, to render the PDFs of the figures from the SVGs, `rsvg-convert`
(package `librsvg`). All commands are run from the repository root.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# runs the analysis notebooks and rewrites their outputs in results/
jupyter nbconvert --to notebook --execute --inplace notebooks/collection/*.ipynb notebooks/rq01/0[0-3]*.ipynb notebooks/rq02/0[1-2]*.ipynb
```

## Reproducing the collection and classification steps

The steps that query GitHub or an LLM are costly. The package allows redoing them in full or on a
sample. In all cases, the output goes to `results/` and is compared with the study's data, which is
not overwritten.

| Step | Command | What it compares | Cost |
|---|---|---|---|
| Ranking (full) | `python -m scripts.ranking.run_ranking` | positions and top 10,000 against `data/collection/ranking/` | ~2 min; requires the SEART export (see `data/collection/README.md`) |
| Detection and download (sample) | `python -m scripts.reproduce_collection_sample` | presence of the formats and content of 100 repositories against the study's collection | ~600 GitHub API requests; requires `GITHUB_TOKEN` in `.env` |
| RQ1 classification (sample) | `python -m scripts.reproduce_classification_sample` | 30 random files against runs 1 to 3 | one Claude Code session |
| Classifier validation (sample) | `python -m scripts.reproduce_classification_sample --validation` | κ of the 97 annotated files against the consensus | four Claude Code sessions |
| RQ2 evidence tracing (sample) | `python -m scripts.reproduce_evidence_sample` | items and categories of 8 random repositories against the study's | one Claude Code session |

After the Claude Code reproductions, run `notebooks/rq01/04_classifier_sample_reproduction.ipynb`
and `notebooks/rq02/03_evidence_sample_reproduction.ipynb`. LLM outputs are not deterministic: the
expected result is an agreement with the study similar to the agreement among the study's own runs.
Detection and download reflect GitHub today, so some files will have changed since 2026.

To redo the detection and download in full, use the scripts of steps 3 and 4 (about 50,000 API
requests). To redo the full classification, follow `data/rq01/README.md`.

## License and citation

Code and data under the MIT license (`LICENSE`). To cite, see `CITATION.cff`.
