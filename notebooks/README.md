# notebooks

Analyses of the paper, one folder per stage. Each notebook states at the top which results of the
paper it reproduces. The outputs go to the corresponding folder in `results/`.

| Notebook | Reproduces |
|---|---|
| `collection/01_adoption_and_download.ipynb` | Repository selection, adoption of the context files, table of formats, and download |
| `rq01/00_sampling_frame.ipynb` | Similarity criterion of the frame of 149 repositories |
| `rq01/01_sample_and_agreement.ipynb` | Sample, κ between annotators, κ of the classifier validation, and agreement across runs |
| `rq01/02_content.ipynb` | Table of categories, co-occurrence (Jaccard), and size by number of categories |
| `rq01/03_formats.ipynb` | Format × category table (repositories with a single file) |
| `rq01/04_classifier_sample_reproduction.ipynb` | Sample-based reproduction of the classifier (optional; requires running `scripts/reproduce_classification_sample.py` first) |
| `rq02/01_agreement_and_relationships.ipynb` | κ between annotators, sample composition, and prevalence of the relationships |
| `rq02/02_evidence_and_conflicts.ipynb` | Evidence by category and conflict types |
| `rq02/03_evidence_sample_reproduction.ipynb` | Sample-based reproduction of the evidence tracing (optional; requires running `scripts/reproduce_evidence_sample.py` first) |

`figures.py` gathers the functions that draw the tables and figures as SVG (and PDF, with
`rsvg-convert`). The notebooks find the repository root by themselves, so they can be opened from any
folder.
