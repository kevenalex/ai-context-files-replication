# data/rq01

Data of RQ1: manual annotation of the sample and classification of the content of the 1,828 files
by an LLM into 13 categories.

## manual_annotation/

| File | Content |
|---|---|
| `rq01_sample_files.csv` | The 97 files of the 47 repositories of the sample (`repo`, `arquivo` = file, `link`). The sample is the same as RQ2's (`data/rq02/rq02_sample_47.csv`). |
| `rq01_manual_labels.csv` | One row per file: categories marked by `anotador_A` (annotator A), by `anotador_B` (annotator B), and the `consenso` (consensus) after discussing the disagreements, each as a comma-separated list. Six files have no consensus and are left out of the comparisons (91 files). |

The labels were recorded in a spreadsheet and exported to CSV.

## classifier/

The classifier is Claude Sonnet, run in Claude Code sessions from the repository root, in batches of
30 files, with the prompt `PROMPT_RQ01_CLASSIFICATION_pt.md`. Part A of the prompt contains the
classification rules (13 categories, disambiguation, and evidence) and Part B, the batch execution
procedure. The prompt was written and used in Portuguese; `PROMPT_RQ01_CLASSIFICATION_en.md` is an
English translation, for reference. Each file receives 0/1 for each category and a literal excerpt as
evidence (`<category>_evidencia`).

| File | Content | Files |
|---|---|---|
| `rq01_validation_run.csv` | Validation: classification of the files of the sample, compared with the annotators' consensus (κ = 0.79) | 97 |
| `rq01_classification_run_1.csv` | Run 1, used in all RQ1 results | 1,828 |
| `rq01_classification_run_2.csv` and `rq01_run_2_log.csv` | Run 2, to measure stability | 1,828 |
| `rq01_classification_run_3.csv` and `rq01_run_3_log.csv` | Run 3, to measure stability | 1,828 |

Column names follow the prompt: `arquivo_analisado` = file label, `link_arquivo` = path of the
classified file in `data/collection/context_files/`, `<category>_evidencia` = evidence, `erro` = error.
The logs record, per batch, the first and last file (`lote_inicio`, `lote_fim`), the number of files
(`arquivos`), the model (`modelo`, `claude-sonnet-5-5`), and the time (`data_hora_utc`).

### How to reproduce the classification

**On a sample** (recommended): `python -m scripts.reproduce_classification_sample` classifies 30
random files, and `--validation` classifies the 97 files of the manual annotation. The script sends
the prompt to Claude Code in non-interactive mode (`claude -p`) with the parameters `EXECUCAO` (run),
`MANIFESTO` (manifest), and `PASTA_SAIDA` (output folder) (see Part B of the prompt). The comparison
with the study is in `notebooks/rq01/04_classifier_sample_reproduction.ipynb`.

**In full** (1,828 files, about 61 batches):

1. Open Claude Code at the repository root with the variable `CLASSIFICACAO_AUTO=<run number>`.
2. Register `continue_classification.py` as a Claude Code *Stop hook*. While there are pending files,
   the hook keeps the session from ending and asks for the next batch.
3. Send the content of `PROMPT_RQ01_CLASSIFICATION_pt.md`, with `EXECUCAO` equal to the run number
   and `PASTA_SAIDA` pointing to a folder outside `data/` (so as not to overwrite the study's runs).

The output of an LLM is not deterministic: repeating the procedure produces similar but not
identical labels (the variation among the three runs is measured in
`notebooks/rq01/01_sample_and_agreement.ipynb`). That is why the paper's results use the frozen
labels of run 1.
