> **English translation, for reference.** The study used the Portuguese version of this prompt
> (`PROMPT_RQ02_EVIDENCE_TRACING_pt.md`), which is the file the reproduction script sends to the model.
> Parameter, column, and label names are kept as in the original.

# Batch prompt — Tracing the RQ2 evidence and mapping it to the RQ1 categories

**How to use:** paste this whole file as the first message of a Claude Code session, from the root
of the repository, giving the parameters below in the same message. Each session processes one
batch and stops. Run the same prompt again, in a new session, to continue where it stopped.

**Parameters**

- `ENTRADA`: labels and evidence from the manual annotation, one repository per row. If not given,
  use `data/rq02/manual_annotation/rq02_labels_annotator_A.csv`.
- `PASTA_SAIDA`: output folder. If not given, use `data/rq02/evidence`.
- Per-repository output: `<PASTA_SAIDA>/rq02_evidence.csv`; long output: `<PASTA_SAIDA>/rq02_evidence_items.csv`.

---

## Context (read before acting)

RQ2 classifies the relationship between the AI context files of the same repository
(`conflitantes` = conflicting, `redundantes` = redundant, `complementares` = complementary). The
manual annotation has already decided, for each repository in the `ENTRADA`, whether each
relationship exists (0/1) and recorded the evidence as free text.

**Your task is not to reclassify.** It is to trace: take each piece of evidence recorded by the
annotator, find in the source files the exact excerpts it refers to, split it into atomic items,
count them, and state which RQ1 content category each item belongs to. The final goal is an RQ1
category × RQ2 relationship matrix (e.g., "conflicts happen mostly in `run_and_build`; redundancy,
in `test_instructions`").

## Step 1 — Read the definitions

1. `data/rq01/classifier/PROMPT_RQ01_CLASSIFICATION_pt.md`, sections A4 and A5 of Part A in full:
   the 13 categories and the disambiguation rules. Use exactly these names:
   `run_and_build`, `project_overview`, `doc_metadata`, `test_instructions`, `project_structure`,
   `system_design`, `contribution_guidelines`, `code_conventions`, `ai_rules`,
   `performance_&_resource_management`, `troubleshooting`, `security`,
   `deployment_&_infrastructure`.
2. The three relationships and the boundary criteria used in the annotation:
   - `complementares`: the files convey distinct information that, together, enriches the agent's context.
   - `redundantes`: the same information is repeated in two or more files, even in different words.
   - `conflitantes`: the files give contradictory instructions on the same aspect of the project.
   - A difference in scope only (the same topic for different cases or tools) is complementary,
     not a conflict.
   - A file that only refers the agent to another one (pointer) is complementary. A cross-reference
     alone is not redundant.
   - The same fact stated twice is redundant, regardless of wording.
   - A different value for the same fact (version, command, name) is conflicting.

## Step 2 — Find out what is left to do

1. Read the `ENTRADA`. Columns:
   `repo, status, qtd_arquivos, arquivos_para_analisar, links_arquivos, conflitantes,
   conflitantes_evidencia, conflitantes_evidencia_qnt, redundantes, redundantes_evidencia,
   redundantes_evidencia_qnt, complementares, complementares_evidencia,
   complementares_evidencia_qnt`.
2. Read the per-repository output (`<PASTA_SAIDA>/rq02_evidence.csv`). If it does not exist, create
   the `PASTA_SAIDA` and the file with the header of Step 4. The repositories already in it are done.
3. Pending = input rows whose `repo` is not yet in the output, in input order.
4. Print how many are done and how many remain (e.g., "12/47 done, 35 pending").

## Step 3 — Run a batch of 8 repositories

For each pending repository:

### 3.1 Locate the files

The repository name comes from the URL in `repo` (`https://github.com/<owner>/<name>`, ignore
anything after it). The folder is `data/collection/context_files/<owner>__<name>/` (letter case may
differ: search case-insensitively). The local file depends on the label in
`arquivos_para_analisar`:

| label | local file |
|---|---|
| `AGENTS.md` | `AGENTS.md` |
| `CLAUDE.md` | `CLAUDE.md` |
| `COPILOT` | `copilot-instructions.md` |
| `CURSOR` | `.cursorrules` |
| `GEMINI.md` | `GEMINI.md` |

Read **all files in full, with line numbers** (e.g., `cat -n`). Do not rely only on keyword
search: the annotator's evidence often paraphrases.

### 3.2 Split the evidence into atomic items

For each relationship (`conflitantes`, `redundantes`, `complementares`) whose `_evidencia` column is
not empty:

- **One item = one unit of information** (a fact, a rule, a command, a topic) involved in that
  relationship. If the annotator joined several topics in one sentence ("Module map,
  spotless:apply, checkstyle:check, jacoco and -pl/-Dtest repeated"), split them into one item per
  topic (here, 5 items). If they split into bullets something that is the same information said
  twice, join it into one item.
- Do not invent items the annotator did not mention, even if you see other overlaps in the files.
  If you notice something relevant that was left out, note it in `observacoes` (Step 4), without
  counting it.
- Generic sentences that point to a topic without detail ("several topics, e.g., Threading, are
  specified in an overlapping way") become one item per topic **that you can locate** in the files
  from the given example. Do not expand to topics the annotator did not name.

### 3.3 Locate each item in the files

For each item, find the literal excerpt(s):

- `conflitantes` and `redundantes`: one excerpt from **each** file involved in the pair.
- `complementares`: the excerpt from the file with the exclusive content (the other file has
  nothing to quote), or both excerpts when they are distinct descriptions of the same topic. For a
  pointer file, quote the delegation line ("See AGENTS.md...").

Mark the status of each item:

- `[OK]` — excerpts found and they support the relationship.
- `[PARCIAL]` (partial) — the topic exists in the files, but the evidence overstates or does not
  support the relationship well (e.g., the evidence says "is repeated almost entirely" and only one
  sentence is repeated; or the "conflict" is one of scope, not of opposite directives). Say why in
  a few words.
- `[NAO_LOCALIZADO]` (not found) — the described text does not exist in the files. Say what you
  searched for.

### 3.4 Assign the RQ1 category

Each item receives **one main RQ1 category**, the one that best describes the content of the
excerpts (not the type of relationship). Use the disambiguation rules of section A4 of the RQ1
prompt (e.g., a command to run tests is `test_instructions`, not `run_and_build`; a rule on the
agent's behavior is `ai_rules`). Examples:

- divergent pnpm versions between files → `run_and_build`
- `m_` prefix vs. `snake_case` with no prefix → `code_conventions`
- "do not mock simple objects" vs. "default to mocks" → `test_instructions`
- pointer file that delegates to another file → `doc_metadata`
- PR flow with `gh pr create` → `contribution_guidelines`

If the item genuinely covers two categories, choose the main one and cite the other in parentheses
as secondary. The matrix count uses only the main one.

### 3.5 Format of each item

One item per line, starting with `- `:

```
- [OK] [run_and_build] pnpm version diverges — AGENTS.md l.14: "pnpm 10.26.2" | CLAUDE.md l.12: "pnpm v10.9.0"
- [OK] [doc_metadata] copilot delegates to AGENTS.md — copilot-instructions.md l.1: "See ../AGENTS.md for project-specific..."
- [PARCIAL] [project_overview] "same" project description — only the first sentence matches — CLAUDE.md l.3: "..." | copilot-instructions.md l.2: "..."
- [NAO_LOCALIZADO] [contribution_guidelines] "never rely on remote names or hard-code origin" — searched in AGENTS.md and copilot-instructions.md, does not exist
```

Short excerpts: enough to check, joined by `[...]` if needed. Never paste paragraphs.

## Step 4 — Write the output

### 4.1 Per-repository output: `<PASTA_SAIDA>/rq02_evidence.csv`

One row per repository, with these columns, in this order:

```
repo, arquivos_para_analisar,
conflitantes, conflitantes_evidencia_tratada, conflitantes_evidencia_qnt, conflitantes_categorias_rq01,
redundantes, redundantes_evidencia_tratada, redundantes_evidencia_qnt, redundantes_categorias_rq01,
complementares, complementares_evidencia_tratada, complementares_evidencia_qnt, complementares_categorias_rq01,
itens_parciais, itens_nao_localizados, observacoes
```

- `repo`, `arquivos_para_analisar`, and the three 0/1 values: copied from the input, unchanged.
- `<relationship>_evidencia_tratada`: the items of Step 3.5, one per line, in the same cell.
  Empty if the relationship is 0 and the evidence is empty.
- `<relationship>_evidencia_qnt`: number of `[OK]` + `[PARCIAL]` items of that relationship.
  `[NAO_LOCALIZADO]` does not count. `0` if there are no items.
- `<relationship>_categorias_rq01`: count by main category, only of the items that count, in the
  format `test_instructions: 2; code_conventions: 1`.
- `itens_parciais`, `itens_nao_localizados`: row totals, adding up the three relationships.
- `observacoes`: inconsistencies worth the annotator's review, for example: relationship marked `1`
  whose items were all `[NAO_LOCALIZADO]`; relationship marked `0` with filled-in evidence (or the
  opposite); a relevant overlap the evidence does not mention.

### 4.2 Long output (one row per item): `<PASTA_SAIDA>/rq02_evidence_items.csv`

```
repo, relacao, item_n, status, categoria_rq01, categoria_rq01_secundaria, descricao,
arquivo_a, linhas_a, trecho_a, arquivo_b, linhas_b, trecho_b
```

- `relacao`: `conflitantes`, `redundantes`, or `complementares`.
- `item_n`: 1, 2, 3... within each repository × relationship.
- `arquivo_b`, `linhas_b`, `trecho_b`: empty when only one file contributes.

Write both outputs in append mode (pandas with `mode="a", header=False`, or equivalent). Never
rewrite the whole file and never reprocess a repository that is already in output 4.1.

## Step 5 — Report at the end of the batch

Report: how many repositories were processed in this session, how many remain, the batch totals
(`OK`, `PARCIAL`, and `NAO_LOCALIZADO` items), and the rows with `observacoes`. Stop here, even if
more would fit.

## Important notes

- Do not change the 0/1 values of the `ENTRADA`. Disagreements go to `observacoes`.
- Identical files (same content): a single redundant item, category = the file's dominant
  category, and note "identical files" in the description.
- An inconsistency within the same file is not a relationship between files: it does not count
  and goes to `observacoes`.
- If the repository folder or a file does not exist, fill `observacoes` with the problem and leave
  the evidence columns empty.
- Everything runs locally from `data/collection/context_files/`. No token is needed.
