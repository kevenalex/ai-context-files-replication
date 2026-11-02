> **English translation, for reference.** The study used the Portuguese version of this prompt
> (`PROMPT_RQ01_CLASSIFICATION_pt.md`), which is the file the reproduction scripts send to the model.
> Parameter and column names are kept as in the original.

# Content classification of AI context files (RQ1)

Batch run with Claude Code, from the root of the repository. This prompt is self-contained: all classification rules are below (Part A), followed by the execution procedure (Part B).

## Goal

Classify the content of each AI context file (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md`, `.cursorrules`) into 13 closed categories. The population is 1,828 files. Each session processes a batch of 30 files and stops; a new session with this same prompt continues where the previous one stopped.

The classification is repeated in independent runs (`EXECUCAO` = 1, 2, or 3) to measure the model's variability. Therefore, each run writes to its own file and must not depend on the others.

---

# Part A — Classification rules

## A1. Role

You are a researcher auditing AI context files of open-source repositories. For each file, identify **which of the 13 content categories (section A5) are present in the text**, with the literal evidence that supports each one.

## A2. Scope rule

**Evaluate only the content of the file itself.** If the file references or points to another file (e.g., `@AGENTS.md`, "See CLAUDE.md for details", a link to `docs/ai/README.md`), **do not explore the content of the referenced file**. The reference itself counts as content (usually `doc_metadata`), but what is inside the referenced file is not considered.

Anchor example: a `CLAUDE.md` whose entire content is the line `@AGENTS.md` (a pure import, Claude Code syntax) must be classified **only** as `doc_metadata`, even if the referenced `AGENTS.md` is long and covers several other categories.

## A3. Procedure for each file

1. Read the file **in full**, from beginning to end, never only the headings or the table of contents. Relevant categories often appear in the middle or at the end of the file.
2. For each of the 13 categories (section A5), ask: *does this file contain a passage that fits the definition of this category?*
3. If so, mark the category as present and record the evidence (section A6).
4. At the end, review: did you reread the whole file or only the top part? If you skipped a section, go back and reread it before finishing.

## A4. Multi-label and disambiguation

The categories are **not mutually exclusive**: the same passage may support more than one category. When genuinely in doubt between two neighboring categories, **mark both**; the risk of missing a category that is actually present is greater than that of marking one too many.

The pairs that cause the most confusion, with the tie-breaking rule:

- **`ai_rules` vs. `code_conventions`**: a rule about *how to write code* (syntax, formatting, naming) is `code_conventions`. A rule about *how the AI agent should behave* (even if the result is code) is `ai_rules`. E.g., "mark AI-generated code blocks with a `// AI:` comment" is `ai_rules`, not `code_conventions`.
- **`security` vs. `code_conventions`**: a rule such as "never hardcode secrets" is `security`, even when phrased as a coding practice.
- **`run_and_build` vs. `test_instructions`**: a command whose purpose is to run or validate tests is `test_instructions`; a generic build or install command is `run_and_build`.
- **`project_overview` vs. `system_design`**: the overview describes *what* the project is; `system_design` describes *how* it is internally structured (patterns, architectural decisions).
- **`performance_&_resource_management` vs. `ai_rules`** *(exclusive pair: choose one)*: performance or resource consumption of the **software being developed** (latency, memory, I/O, benchmarks) is `performance_&_resource_management`. Concern with the cost or consumption of the **agent's own tokens** while performing the task (e.g., "avoid re-deriving deterministic information on every run so as not to waste tokens") is about the agent's behavior: mark `ai_rules`, not `performance_&_resource_management`.
- **`system_design` vs. `ai_rules`** *(exclusive pair: choose one)*: a passage that **describes** the architecture or patterns of the system (data flow, layers, design patterns) is `system_design`. A passage that **instructs the agent's behavior** when working on that architecture (e.g., "do not hallucinate AST formats, check identifiers before using them") is `ai_rules`, even if it mentions internal components of the system.
- **`contribution_guidelines` vs. `ai_rules`** *(additive pair: mark both when applicable)*: a PR or commit process that applies to any contributor (human or AI) is `contribution_guidelines`. A rule that only makes sense for an AI agent (e.g., "AIs must identify themselves as such in the PR description") is **also** `ai_rules`, without removing `contribution_guidelines`.

> **Important:** only the two pairs marked as *exclusive* follow the "one or the other" model. All other pairs, including `contribution_guidelines` vs. `ai_rules`, are **additive**: the fact that a passage qualifies as `ai_rules` is no reason to remove or not mark another category that also applies. Do not generalize the "choose one" pattern to other pairs. Treat each category in section A5 as an independent question (step 2 of section A3).

## A5. Vocabulary of the 13 categories

| Category | Definition | Anchor example |
|---|---|---|
| `run_and_build` | Instructions for building the application; dependency management; instructions on how to run the application. | `"Run pnpm build to build all packages"; "Run pnpm install to install dependencies"` |
| `project_overview` | Description of the tool; context on the use of the repository; main tools, languages, and dependencies the software uses. | `"Project Overview — Vitest is a next-generation testing framework powered by Vite..."` |
| `doc_metadata` | Documentation latent to code specifications; references to **other** documentation files or folders (including other AI context files). The standard self-description sentence of the file itself (e.g., "This file provides guidance to Claude Code when working with code in this repository") **does not count**, as it is only the introductory header. | `"Essential references — Agent-specific guide: See AGENTS.md"` |
| `test_instructions` | How to write tests; how tests work in the project; where tests are located in the file structure; how to run tests. | `"pnpm test packages/react-router/__tests__/router/fetchers-test.ts  # Single file"` |
| `project_structure` | Physical organization of the repository's files and directories. | `"Project Structure — kotest-common/  # Shared annotations..."` |
| `system_design` | Project patterns; design patterns and the like (internal architecture). | `"Follow ChurchCRM patterns: Use Perpl ORM (never raw SQL)..."` |
| `contribution_guidelines` | Branch and commit conventions; external contribution process (CLA, PR and issue templates, requirements for PR acceptance). | `"All contributors must review the CLA and sign it by adding their github username to contributors.yml"` |
| `code_conventions` | Syntax guides for the code produced; formatting; naming style (camelCase, PascalCase, etc.). | `"Do not add one-line comments unless you think they are really useful"` |
| `ai_rules` | Instruction designed exclusively for the LLM: it does not describe the system's logic, but how the LLM should act in specific scenarios. | `"AI-generated source code blocks must be marked with // AI: below section was generated by an AI"` |
| `performance_&_resource_management` | Pipeline execution costs; usage or implementation constraints due to hardware; optimizations. | `"This is a performance-critical testing framework — Pay attention to import costs and bundle size"` |
| `troubleshooting` | Solutions to common problems with the application or the tools used by the system. | `"Ensure pnpm is used (not npm/yarn); Build before running tests"` |
| `security` | Authentication, authorization, and access control; input validation and protection against common vulnerabilities; handling of sensitive data; vulnerability disclosure policy. | `"Security first: Check authorization, input validation, and data sensitivity for every change"` |
| `deployment_&_infrastructure` | CI and CD specifications; deployment specifications. It must be an **actual instruction or specification** (pipeline, command, process). A passing mention of where the application runs in production (e.g., "the system runs in Kubernetes in production") without detailing the process **does not count**; that is `project_overview` or `system_design`. | `"Push to main triggers .github/workflows/server-production-deployment.yml, which cascades canary → acceptance tests → production"` |

## A6. Evidence rule

Every category marked as present needs **literal** evidence (a direct quotation from the text, not a paraphrase). If the category appears in more than one passage, **join the passages in a single cell, concisely**: short excerpts separated by ` [...] `, never the whole paragraph pasted. The target is 3 to 5 lines of evidence per category.

## A7. Edge cases

- **Pure pointer file** (`@AGENTS.md`, "See CLAUDE.md for complete instructions"): receives only `doc_metadata` (section A2). This is the expected result, not an error.
- **Generic content, unrelated to the repository** (e.g., a `CLAUDE.md` that only describes how Claude Code should parallelize its tasks, with nothing specific to the project): classify it by what it actually contains (typically `ai_rules`), even if the content is not useful or specific.

## A8. When in doubt

If, after applying the disambiguation rules (section A4), there is still genuine uncertainty about a category, prefer marking it as present with weaker evidence over leaving it out, but never mark a category without some literal quotation that supports it. Never infer a category from the absence of content (e.g., do not mark `security` just because the project seems to handle sensitive data); the category needs an actual passage in the text.

---

# Part B — Execution

## B1. Parameters

- `EXECUCAO`: run identifier (1, 2, or 3; `sample` or `validation` in the sample reproduction), given in the same message as this prompt. If it was not given, stop and ask.
- `MANIFESTO`: list of files to classify. If not given, use `data/collection/context_files/download_manifest.csv`.
- `PASTA_SAIDA`: folder of the output files. If not given, use `data/rq01/classifier`.
- Output file: `<PASTA_SAIDA>/rq01_classification_run_<EXECUCAO>.csv`
- Log file: `<PASTA_SAIDA>/rq01_run_<EXECUCAO>_log.csv`, with the columns `lote_inicio`, `lote_fim`, `arquivos`, `modelo`, `data_hora_utc`.

## B2. Independence rules

- Read only this prompt, the list of downloaded files (`download_manifest.csv`, see section B3), the files to classify, and the output file of this run. Do not open other files of the repository (in particular manual labels, previous classifications, outputs of other runs, and the old RQ1 guide), so that the classification is not influenced by existing labels.
- Classify each file only by what is written in it and by the rules of Part A. Do not use external knowledge about the repository.
- Do not reclassify a `(repo, arquivo_analisado)` pair that is already in the output file of this run.

## B3. Identify the pending files

1. Read the `MANIFESTO` (columns `repo`, `file_label`, `local_path`, `status`) and keep only the rows with `status == "ok"`. The full manifest has 1,828 files. The file path is built as in B4.
2. If the output file of this run exists, read the `(repo, arquivo_analisado)` pairs already in it. If it does not exist, create the `PASTA_SAIDA` and the file with the header of B5.
3. The pending files are the manifest rows whose `(repo, file_label)` pair is not in the output file, in manifest order.
4. Report how many files have already been classified and how many remain (e.g., "347/1828 done, 1481 pending").

## B4. Classify a batch

Take the next 30 pending files. For each one:

1. Locate the file at `data/collection/context_files/<repo with "/" replaced by "__">/<local_name>`, where `local_name` depends on the `file_label`:

   | `file_label` | `local_name` |
   |---|---|
   | `AGENTS.md` | `AGENTS.md` |
   | `CLAUDE.md` | `CLAUDE.md` |
   | `COPILOT` | `copilot-instructions.md` |
   | `CURSOR` | `.cursorrules` |
   | `GEMINI.md` | `GEMINI.md` |

   Example: `elastic/elasticsearch` with `AGENTS.md` is at `data/collection/context_files/elastic__elasticsearch/AGENTS.md`.

2. Classify the file following Part A (procedure of section A3). The classification is done by you, reading and interpreting the text: do not use scripts, regular expressions, or keyword search to assign categories, and do not delegate the classification to subagents. Scripts are only for listing pending files and for writing and checking the CSV.
3. Use the `erro` column only when the file cannot be read; in that case, describe the problem in a few words and leave the category columns empty. Empty files or pure pointers are not errors: follow section A7.

## B5. Write the result

Append one row per file to the end of the output file. Never rewrite the whole file. Write with Python's `csv` module (`csv.writer`, UTF-8, `newline=""`), never by concatenating text, because the evidence contains commas, quotes, and line breaks.

Columns, in this exact order:

```
repo, arquivo_analisado, link_arquivo,
run_and_build, run_and_build_evidencia,
project_overview, project_overview_evidencia,
doc_metadata, doc_metadata_evidencia,
test_instructions, test_instructions_evidencia,
project_structure, project_structure_evidencia,
system_design, system_design_evidencia,
contribution_guidelines, contribution_guidelines_evidencia,
code_conventions, code_conventions_evidencia,
ai_rules, ai_rules_evidencia,
performance_&_resource_management, performance_&_resource_management_evidencia,
troubleshooting, troubleshooting_evidencia,
security, security_evidencia,
deployment_&_infrastructure, deployment_&_infrastructure_evidencia,
erro
```

- `repo`: value of `repo` in the manifest.
- `arquivo_analisado`: value of `file_label` in the manifest.
- `link_arquivo`: `local:<file path, relative to the repository root>`.
- Category columns: `1` or `0`.
- Evidence columns: literal quotation (section A6) if the category is present; empty if it is absent.
- `erro`: empty, except in the case described in B4.

After writing, append a row to the log file with the first and last file of the batch, the number of files, the model identifier of this session, and the date and time in UTC.

## B6. Check the batch

Before finishing, check with a script the rows you have just written:

- each row has exactly 30 columns (3 identification columns, 26 category and evidence columns, and `erro`);
- the category columns contain only `0` and `1`;
- every category `1` has evidence and every category `0` has empty evidence;
- there are no duplicate `(repo, arquivo_analisado)` pairs in the output file.

Fix any inconsistency before moving on.

## B7. Report and continue

Report how many files were classified in this session, how many remain in total, and whether any file had an error (and which one). Run the prompt again for the next batch.
