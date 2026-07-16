# Scripts

Módulos de processamento (lógica central) e scripts de entrada (`run_*.py`) do pipeline de pesquisa. Ver `README.md` na raiz do projeto para o fluxo de execução completo (Etapas 1-3).

## Atribuição de Código

- **`ranking.py`**: O algoritmo de ranqueamento (score de popularidade + maturidade, com penalidades para repositórios educacionais/baixo teor de código) foi copiado/adaptado do material suplementar do artigo *"Context Engineering for AI Agents in Open-Source Software"*, disponível em https://zenodo.org/records/18368326 (arquivo `1_data-collection/ranking.py`).

- **`extract_content_structure.py`** e **`classify_headings.py`**: Inspirados na etapa de análise de estrutura de cabeçalhos do mesmo material suplementar (pasta `3_rq2/`, scripts `heading_level_analysis.py` e `heading_stats.py`, referente à RQ2 do artigo original — "What information do open-source developers provide in AI context files and how do they present it?"). O código aqui **não é uma cópia**: é uma reimplementação independente e mais simples, com as seguintes diferenças/acréscimos em relação ao original:
  - Extração de cabeçalhos via Regex sobre o Markdown bruto, em vez de um parser CommonMark (`markdown_it`) com rastreamento de hierarquia de pais (`path_norm`).
  - Sem filtro de idioma (o original usa a biblioteca `lingua` para excluir arquivos/cabeçalhos não primariamente em inglês) e sem lematização dos termos normalizados (o original usa `nltk.WordNetLemmatizer` para unificar variações como "test"/"tests"/"testing").
  - Processa os 5 tipos de arquivo de contexto (`AGENTS.md`, `CLAUDE.md`, Copilot instructions, `GEMINI.md`, `.cursorrules`), enquanto o original processa apenas `AGENTS.md`.
  - A taxonomia de categorias em `classify_headings.py` é uma classificação **automática por palavra-chave**, com nomes de categoria inspirados conceitualmente no material de referência; o original chegou às suas categorias por **codificação qualitativa manual** dos pesquisadores (`headings_aggregated.xlsx`, com guia de codificação documentado).

- **`detect_ai_context_files/detect_via_api.py`** e **`detect_ai_context_files/detect_via_clone.py`**: Conceitualmente equivalentes ao script `collect_ai_configs.py` do mesmo material suplementar (pasta `1_data-collection/`), que também detecta arquivos de contexto de IA via clonagem rasa (`git clone --depth=1`). O código aqui também **não é uma cópia** — é uma reimplementação independente, mais simples e dividida em duas estratégias (API REST vs. clonagem), com as seguintes diferenças:
  - **Caminho fixo vs. varredura completa:** ambos os nossos scripts verificam apenas um caminho candidato fixo por tipo de arquivo (ex: `AGENTS.md` na raiz, `.github/copilot-instructions.md`). O original faz `os.walk` na árvore inteira do repositório com Regex, encontrando os arquivos em qualquer subdiretório e suportando múltiplas ocorrências por repositório (nós registramos apenas presença binária 0/1; o original registra os links reais do GitHub para cada ocorrência, unidos por `;`).
  - **Detecção vs. coleta combinadas:** o original já copia o conteúdo dos arquivos encontrados para uma pasta de saída local (fundindo detecção + coleta de conteúdo numa única etapa) e identifica arquivos "apenas-redirecionamento" (`is_pointer_only_md`, sem cabeçalho Markdown). Nos nossos scripts essas etapas são separadas: a detecção (`detect_via_api.py`/`detect_via_clone.py`) só marca presença; o conteúdo é buscado depois, à parte, em `extract_content_structure.py` — e não há detecção de arquivos-redirecionamento.
  - **Conjunto de arquivos monitorados:** o original verifica `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md` e `.github/instructions/*.md` (convenção mais nova de múltiplos arquivos de instrução), mas **não** verifica `.cursorrules`. Foi adicionado o `.cursorrules` (`CURSOR`) por exemplo.
  - **Paralelismo:** `detect_via_clone.py` usa `ThreadPoolExecutor` (assim como o original) para clonar/verificar em paralelo; `detect_via_api.py` é sequencial, já que o gargalo nesse caso é o rate limit da API do GitHub, não fork de processos — uma estratégia que não tem equivalente direto no original (que evita a API REST inteiramente, preferindo clone local).

## Demais Scripts

- `ranking/run_ranking.py`: Script de entrada da Etapa 1 — configura `INPUT_FILE`/`OUTPUT_FOLDER` e chama `rank_repositories()`.
- `detect_ai_context_files/run_detect_context.py`: Script de entrada da Etapa 2 — escolhe o modo (`API` ou `CLONE`) e orquestra a detecção.
- `extract_testing_details.py`: Extração de dados para validação de fidelidade de testes (Etapa 3).
