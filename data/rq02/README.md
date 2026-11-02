# data/rq02

Data of RQ2: frame and sample of repositories with two or more files, manual annotation of the
relationships between the files, and evidence. The same sample is used in the RQ1 annotation.

| File | Content | Origin |
|---|---|---|
| `rq02_population_487.csv` | The 487 repositories with two or more detected files (`repo`, `qtd_arquivos` = number of files, `arquivos_para_analisar` = files to analyze). | detection (`data/collection/detection/`) |
| `rq02_frame_149.csv` | Frame from which the sample was drawn: 185 file pairs in 149 repositories (columns `repo`, `file1`, `file2`; the other columns come from an exploratory probe and are not used in the paper). | see below |
| `rq02_sample_47.csv` | The pairs of the frame that belong to the 47 sampled repositories. | `scripts/sample_manual_validation.py` |
| `manual_annotation/rq02_labels_annotator_A.csv` | Labels of annotator A: for each repository, 0/1 for each relationship, with the evidence of each one. These are the reference labels of the results. | annotation spreadsheet |
| `manual_annotation/rq02_labels_annotator_B.csv` | Labels of annotator B, in the same format. Used for κ. | annotation spreadsheet |
| `evidence/rq02_evidence.csv` | For each repository, the marked relationships and the recorded evidence, reviewed. | manual annotation |
| `evidence/rq02_evidence_items.csv` | The evidence split into items: relationship, RQ1 category, excerpts and lines in the two files, and `status` of the excerpt location. | Claude Code with `evidence/PROMPT_RQ02_EVIDENCE_TRACING_pt.md`, from the labels of annotator A |

The evidence tracing can be redone on a sample with `python -m scripts.reproduce_evidence_sample`
(see the root `README.md`). The prompt was written and used in Portuguese;
`evidence/PROMPT_RQ02_EVIDENCE_TRACING_en.md` is an English translation, for reference.

## Column names and labels

The files keep the column names of the annotation spreadsheet, in Portuguese:

| Name | Meaning |
|---|---|
| `conflitantes`, `redundantes`, `complementares` | conflicting, redundant, complementary (0/1) |
| `<relationship>_evidencia` | evidence recorded by the annotator (free text, in Portuguese) |
| `<relationship>_evidencia_qnt` | number of evidence items |
| `status` (labels) | `Finalizado` = finished |
| `relacao`, `categoria_rq01`, `descricao` | relationship, RQ1 category, description |
| `arquivo_a`, `linhas_a`, `trecho_a` (and `_b`) | file, lines, and excerpt in each file |
| `status` (items) | `OK`; `PARCIAL` = partial; `NAO_LOCALIZADO` = not found; `DESCARTADO` = discarded |
| `observacoes` | notes |

## Frame of 149 repositories

The frame was computed in May 2026 on the content read live from GitHub:

1. of the 487 repositories, we kept the file pairs with both files above 92.95 characters (P35):
   262 pairs in 205 repositories;
2. of these, we kept the pairs with textual similarity (`difflib.SequenceMatcher`) of at most 0.5:
   185 pairs in 149 repositories.

The content read in May was not stored, and the list of the 205 repositories was not saved. The
frame is therefore distributed as frozen data. `notebooks/rq01/00_sampling_frame.ipynb` shows the
similarity criterion with the files downloaded in June.

## Sample selection

`scripts/sample_manual_validation.py` computes the sample size with Cochran's formula with finite
population correction (90% confidence, 10% margin: 47 repositories) and draws the repositories with
seed 42. Running the script recreates `rq02_sample_47.csv` identically. The repository
`wled-dev/WLED` was renamed `wled/WLED` on GitHub after the sample was drawn.
