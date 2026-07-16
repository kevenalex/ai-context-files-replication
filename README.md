# Engenharia de Contexto para Agentes de IA: Adoção, Sobreposição e Estrutura de Arquivos de Contexto em Repositórios de Código Aberto - **PESQUISA EM ANDAMENTO**

Este projeto tem como objetivo analisar como repositórios populares de código aberto utilizam arquivos de configuração para agentes de IA, como AGENTS.md, CLAUDE.md, GEMINI.md, etc, e com isso identificar padrões de uso e inferências da qualidade e segurança destes projetos.

## Estrutura do repositório
- `data/`: Centraliza todos os dados brutos e processados da pesquisa (ver detalhamento abaixo).
- `notebooks/`: Jupyter notebooks numerados na ordem do pipeline (`1-...` a `7-...`), mais `notebooks/research_questions/<rq>/` para o aprofundamento de cada questão de pesquisa.
- `results/`: Resultados consolidados da pesquisa (gráficos, tabelas, artigo compilado).
- `scripts/`: Scripts geradores/processadores de dados que alimentam os notebooks do projeto (ver "Fluxo de Trabalho" abaixo).
- `docs/`: Documentação de apoio ao processo de pesquisa (ex.: checklist de correções/reprodutibilidade).
- `LICENSE` / `CITATION.cff`: Termos de licenciamento e informações de citação do repositório.
- `.env`: Arquivo de variável de ambiente reservado para as seguintes variáveis usadas pela pesquisa (Arquivo criado apenas em ambiente local):
  - `GITHUB_TOKEN`;
  - `GEMINI_API_KEY`.

### Especificação da pasta `data/`

A pasta `data/` tem apenas dois diretórios no topo — `oldData/` e `newData/` — correspondendo a duas coletas SEART (a coleta antiga e a nova, em processo de transição). Ambos espelham a mesma estrutura interna:

- `input_data/`: Dado bruto de entrada, intocável — JSON exportado da ferramenta SEART.
- `rq01/`: Dados da **RQ1** do artigo ("Natureza temática das diretrizes"), incluindo todo o pipeline que a alimenta:
  - `output_rankings/`: Repositórios ranqueados (Etapa 1).
  - `ai_context_files_in_repositories/`: Detecção binária de arquivos de contexto de IA (Etapa 2).
  - `rq00/`: Conteúdo bruto baixado de cada arquivo detectado, mais o `download_manifest.csv`.
  - `structure_analysis.csv` / `structure_analysis_classified.csv`: Cabeçalhos extraídos e classificados por categoria.
  - `regex_analysis_content_ai_context_files.csv`: Classificação temática por repositório.
- `rq02/`: Dados da **RQ2** do artigo ("Sobreposição lexical e semântica em múltiplos arquivos de contexto"): `semantic_analysis_rq01.csv` e os artefatos de revisão manual (amostra, planilha cega, checklist por repositório).
- `misc/`: Dados que não pertencem a nenhuma RQ do artigo (ex.: `testing_analysis/`, estudo de validade dos testes automatizados).

## Stack Tecnológica (Tech Stack)
- **Linguagem:** Python 3.14
- **Bibliotecas Principais:** Pandas 3.0.2, NumPy 2.4.4, Requests 2.33.1, python-dotenv 1.2.2.
- **Visualização:** Matplotlib 3.10.9, Seaborn 0.13.2, Jupyter 1.1.1.
- **Análise Semântica (RQ2):** google-genai 1.75.0 (SDK do Gemini, usado em `notebooks/research_questions/rq02/notebook.ipynb`).
- Versões fixadas em `requirements.txt` (via `pip freeze`) para garantir reprodutibilidade.

## Configuração e Instalação (Setup)

> Todos os comandos abaixo devem ser executados a partir da **raiz do repositório**.

1. Criar ambiente virtual: `python -m venv .venv`
2. Ativar ambiente: `source .venv/bin/activate`
3. Instalar dependências: `pip install -r requirements.txt`
4. Configurar `.env`: criar um arquivo `.env` na raiz do projeto com `GITHUB_TOKEN=seu_token` e `GEMINI_API_KEY=seu_token`.
   
## Fluxo de Trabalho (Workflow)
O processo segue estas etapas, em ordem:

1. **Ranqueamento (Etapa 1):** 
   - **Objetivo:** Lê os dados brutos e define os repositórios mais importantes (maduros e populares).
   - **Arquivo:** `scripts/ranking/run_ranking.py`
   - **Variáveis principais:** `INPUT_FILE` (em `data/newData/input_data/` ou `data/oldData/input_data/`), `OUTPUT_FOLDER` (`data/newData/rq01/output_rankings/` ou `data/oldData/rq01/output_rankings/`, conforme a coleta processada).
   - **Execução:** `python -m scripts.ranking.run_ranking` (a partir da raiz do projeto — necessário rodar como módulo por causa do import `scripts.ranking.ranking`).

2. **Detecção (Etapa 2):** 
   - **Objetivo:** Verifica quais repositórios do ranking possuem arquivos para IA.
   - **Arquivo:** `scripts/detect_ai_context_files/run_detect_context.py`
   - **Variáveis principais:** `MODE` ("API" ou "CLONE"), `INPUT_CSV` (CSV gerado na Etapa 1, em `data/newData/rq01/output_rankings/` ou `data/oldData/rq01/output_rankings/`), `OUTPUT_FOLDER` (`data/newData/rq01/ai_context_files_in_repositories/` ou `data/oldData/rq01/ai_context_files_in_repositories/`).
   - **Execução:** `python -m scripts.detect_ai_context_files.run_detect_context` (a partir da raiz do projeto — necessário rodar como módulo pelos mesmos motivos da Etapa 1).

3. **Coleta de Conteúdo Bruto (Etapa 3):**
   - **Objetivo:** Baixar o conteúdo real de cada arquivo de contexto detectado na Etapa 2.
   - **Arquivo:** `scripts/download_ai_context_files.py`
   - **Variáveis principais:** `INPUT` (CSV da Etapa 2), `OUTPUT_DIR` (`data/oldData/rq01/rq00/` ou `data/newData/rq01/rq00/`).
   - **Saída:** Um arquivo por repositório/tipo de contexto baixado, mais um `download_manifest.csv` na mesma pasta.
   - **Execução:** `python -m scripts.download_ai_context_files`.

4. **Análise de Conteúdo — RQ1 (Etapa 4):**
   - **Objetivo:** Classificar tematicamente as diretrizes coletadas (natureza temática das diretrizes).
   - **Scripts:**
     - `scripts/regex_analysis_content.py`: classifica, por repositório, quais categorias temáticas (ex.: "Testing Instructions", "Architecture") aparecem nos arquivos baixados na Etapa 3. **Entrada:** `rq00/download_manifest.csv`. **Saída:** `rq01/regex_analysis_content_ai_context_files.csv`.
     - `scripts/extract_content_structure.py`: extrai os cabeçalhos Markdown de cada arquivo de contexto de IA via API do GitHub. **Entrada:** CSV da Etapa 2. **Saída:** `rq01/structure_analysis.csv`.
     - `scripts/classify_headings.py`: classifica semanticamente cada cabeçalho extraído na mesma taxonomia usada por `regex_analysis_content.py`. **Entrada:** `rq01/structure_analysis.csv`. **Saída:** `rq01/structure_analysis_classified.csv`.
   - **Execução:** cada script é executado diretamente (`python -m scripts.<nome_do_script>`), ajustando as variáveis `INPUT`/`OUTPUT` no bloco `if __name__ == "__main__"`.

5. **Validação de Fidelidade de Testes (Etapa 5, `misc`):**
   - **Objetivo:** Auditar se as instruções de teste presentes nos arquivos de contexto realmente correspondem ao processo de teste do repositório (checagem de validade, não é uma RQ do artigo).
   - **Arquivo:** `scripts/extract_testing_details.py`
   - **Entrada:** `rq01/structure_analysis_classified.csv`. **Saída:** `misc/testing_analysis/testing_validity_data.json`.

6. **Amostragem e Revisão Manual — RQ2 (Etapa 6):**
   - **Objetivo:** Selecionar e preparar uma amostra estatisticamente significativa de repositórios com múltiplos arquivos de contexto para revisão manual de sobreposição lexical/semântica.
   - **Scripts:**
     - `scripts/sample_manual_validation.py`: calcula o tamanho da amostra pela fórmula de Cochran (com correção para população finita) e sorteia os repositórios. **Entrada:** `rq02/semantic_analysis_rq01.csv`. **Saída:** `rq02/sample.csv`.
     - `scripts/build_manual_review_sheet.py`: monta uma planilha "cega" (sem indicar a classificação automática) com links diretos para os arquivos de cada repositório amostrado. **Entrada:** `rq02/sample.csv`. **Saída:** `rq02/manual_review_blind.csv`.
     - `scripts/build_repo_checklist.py`: consolida um checklist por repositório (um repositório pode ter mais de um par de arquivos a revisar). **Entrada:** CSV de amostra com links. **Saída:** `rq02/repo_checklist.csv`.
   - **Execução:** cada script é executado diretamente (`python -m scripts.<nome_do_script>`), ajustando as variáveis `INPUT`/`OUTPUT` no bloco `if __name__ == "__main__"`.

### Etapa 1: Ranqueamento de Repositórios

Nesta etapa, o script lê os dados brutos e define quais são os repositórios mais importantes (maduros e populares).

Como usar:
1. Abra o arquivo scripts/ranking/run_ranking.py.
2. Altere a variável INPUT_FILE para o caminho do seu arquivo JSON (ex: "data/newData/input_data/dados.json" ou "data/oldData/input_data/dados.json").
3. Salve o arquivo e execute no terminal - a partir da raiz do projeto:
  > python -m scripts.ranking.run_ranking

Exemplo de Entrada: Um arquivo JSON com milhares de repositórios do GitHub.
Exemplo de Saída: Um arquivo CSV na pasta `output_rankings/` (dentro de `data/newData/rq01/` ou `data/oldData/rq01/`, conforme a coleta) contendo os repositórios ordenados por uma pontuação (rank_score).

### Etapa 2: Detecção de Contexto de IA

Nesta etapa, o script pega a lista gerada na Etapa 1 e verifica quais daqueles repositórios possuem arquivos para IA.

Como usar:
1. Abra o arquivo scripts/detect_ai_context_files/run_detect_context.py.
2. Defina o MODE como "API" ou "CLONE".
3. Ajuste a variável INPUT_CSV para apontar para o arquivo gerado na Etapa 1.
4. Salve o arquivo e execute no terminal - a partir da raiz do projeto:
  > python -m scripts.detect_ai_context_files.run_detect_context

Exemplo de Entrada: O arquivo CSV gerado pelo ranking (ex: ranked_dados.csv).
Exemplo de Saída: Um novo arquivo CSV na pasta `ai_context_files_in_repositories/` (dentro de `data/newData/rq01/` ou `data/oldData/rq01/`) com colunas indicando 0 ou 1 para a presença de arquivos como AGENTS.md e CLAUDE.md.

### Etapas 3 a 6: Coleta de Conteúdo, Análise Temática, Validação de Testes e Amostragem

Ver a descrição detalhada de cada script na seção "Fluxo de Trabalho" acima. Todos seguem o mesmo padrão de uso: abrir o script, ajustar as variáveis `INPUT`/`OUTPUT` (ou `INPUT_CSV`/`MANIFEST`, conforme o caso) no bloco `if __name__ == "__main__":` e executar com `python -m scripts.<caminho_do_script>` a partir da raiz do projeto.

### Etapa 7: Análise e Visualização

Nesta etapa, utilizamos os notebooks para transformar os dados coletados em gráficos e insights.

Como usar:
1. Com o ambiente virtual ativo, execute: `jupyter notebook`
2. Abra a pasta `notebooks/` e escolha um dos arquivos, seguindo a numeração do pipeline:
  - `1-seart_data_study.ipynb`: Estudo exploratório dos dados brutos do SEART.
  - `2-ranking_data_study.ipynb`: Estudo dos dados ranqueados (Etapa 1).
  - `3-context-ai-repo-study.ipynb`: Análise de adesão — percentual de repositórios com arquivos de contexto de IA (Etapa 2).
  - `4-structure_analysis_study.ipynb`: Estudo da estrutura de cabeçalhos extraída (Etapa 4).
  - `4.1-structure_analysis_quantitative.ipynb`: Análise quantitativa complementar dos cabeçalhos (distribuição por nível, tópicos mais comuns, comparação entre tipos de arquivo — Etapa 4).
  - `5-ai-file-classification-study.ipynb`: Estudo da classificação temática dos cabeçalhos (Etapa 4).
  - `6.1-test-validity-checker.ipynb`: Checagem da validação de fidelidade de testes (Etapa 5).
  - `7-repo_level_category_study.ipynb`: Estudo da classificação temática por repositório (Etapa 4, `regex_analysis_content.py`).
  - `8-analysis_comparison.ipynb`: Compara resultados de coletas diferentes (`oldData` vs. `newData`) para mostrar a evolução temporal da adesão.
  - `research_questions/rq02/notebook.ipynb`: Notebook de aprofundamento da RQ2 do artigo (análise semântica via LLM e amostragem para revisão manual).

## Uso do Token do GitHub

Para evitar bloqueios por excesso de acessos na API do GitHub, você deve:
1. Criar um arquivo chamado .env na raiz do projeto.
2. Escrever dentro dele: GITHUB_TOKEN=seu_token_aqui

## Artefatos Publicados

Além do código e dos dados processados neste repositório, os dados brutos do SEART e a planilha de revisão manual da RQ2 (mantida à parte, fora do controle de versão) estão publicados no Zenodo, sob o DOI [10.5281/zenodo.21388606](https://doi.org/10.5281/zenodo.21388606).

> **Acesso:** o registro no Zenodo é público, mas o acesso aos arquivos é **privado por decisão do autor**. Caso o acesso seja necessário, ele deve ser solicitado diretamente pela página do depósito no Zenodo.

## Como Citar

Este repositório é licenciado sob os termos do arquivo [`LICENSE`](./LICENSE) (MIT). Para citar este trabalho, utilize as informações do arquivo [`CITATION.cff`](./CITATION.cff) ou a referência abaixo:

> SANTOS, Keven Alex Barbosa. **Engenharia de Contexto para Agentes de IA: Adoção, Sobreposição e Estrutura de Arquivos de Contexto em Repositórios de Código Aberto**. Universidade Federal de Campina Grande, 2026. Disponível em: https://github.com/kevenalex/tcc. DOI: [10.5281/zenodo.21388606](https://doi.org/10.5281/zenodo.21388606).

---
