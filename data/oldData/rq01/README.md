# RQ1 — Natureza Temática das Diretrizes

## Contexto
Esta pasta reúne todo o pipeline de dados da RQ1 do artigo ("Qual é a natureza temática das diretrizes documentadas nos arquivos de contexto de IA?"): desde o ranqueamento e a detecção que definem a população de repositórios, até a extração e classificação de conteúdo propriamente ditas.

## Arquivos e subpastas
1. **`output_rankings/`**: CSVs gerados por `scripts/ranking/run_ranking.py` (Etapa 1) — repositórios ordenados por `rank_score`.
2. **`ai_context_files_in_repositories/`**: CSVs gerados por `scripts/detect_ai_context_files/run_detect_context.py` (Etapa 2) — detecção binária (0/1) de `AGENTS.md`, `CLAUDE.md`, `COPILOT`, `GEMINI.md`, `CURSOR` por repositório.
3. **`rq00/`**: Conteúdo bruto (Markdown) dos arquivos de contexto efetivamente baixados por `scripts/download_ai_context_files.py`, um subdiretório por repositório.
4. **`structure_analysis.csv`**: Hierarquia de títulos extraída via Regex sobre o Markdown bruto (`scripts/extract_content_structure.py`).
   - Colunas: `repo`, `file_type`, `level` (#, ##, ###), `title_original`, `title_normalized`.
5. **`structure_analysis_classified.csv`**: Adiciona classificação temática por palavra-chave sobre o arquivo anterior (`scripts/classify_headings.py`).
   - Coluna adicional: `category` (ex: `Testing Instructions`, `Architecture / Project Structure`, `Code Conventions / Best Practices`).
6. **`regex_analysis_content_ai_context_files.csv`** / **`outliers_amplitude_categorias.csv`**: Agregação por repositório (não por cabeçalho) das categorias de conteúdo, gerada por `scripts/regex_analysis_content.py` a partir do manifesto de `rq00/`.

## Uso
Consumido pelos notebooks `3-context-ai-repo-study.ipynb`, `4-structure_analysis_study.ipynb`, `5-ai-file-classification-study.ipynb` e `7-repo_level_category_study.ipynb`. Serve também de base para a amostragem da RQ2 (`data/oldData/rq02/`).
