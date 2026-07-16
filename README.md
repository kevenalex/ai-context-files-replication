# Engenharia de Contexto para Agentes de IA: Adoção, Sobreposição e Estrutura de Arquivos de Contexto em Repositórios de Código Aberto - **PESQUISA EM ANDAMENTO**

Este projeto tem como objetivo analisar como repositórios populares de código aberto utilizam arquivos de configuração para agentes de IA, como AGENTS.md, CLAUDE.md, GEMINI.md, etc, e com isso identificar padrões de uso e inferências da qualidade e segurança destes projetos.

## Estrutura do repositório
- `data/`: Centraliza todos os arquivos de dados a serem analisados do projeto.
- `notebooks/`: Espaço reservado para o armazenamento de jupyter notebooks do tipo <xpto.ipynb>, scripts estes pivôs da análise e interpretação dos resultados desta pesquisa.
- `results/`: Diretório reservado para o armazenamento de resultados de análise dos dados da pesquisa, como gráficos e tabelas geradas pelas análises dos notebooks.
- `scripts/`: Scripts geradores/processadores de dados para alimentação dos databases dos notebooks do projeto.
- `.env`: Arquivo de variável de ambiente reservado para as seguintes variáveis usadas pela pesquisa (Arquivo criado apenas em ambiente local):
  - `GITHUB_TOKEN`;
  - `GEMINI_API_KEY`.

### Especificação da pasta `data/`:

- Estrutura geral:
  - `data/`: Centraliza todos os arquivos de dados a serem analisados do projeto.
    - `input_data/`: Dados brutos de entrada - JSON correspondente aos repositórios resultantes da pesquisa da ferramenta SEART.
    - `analysis_data/`: Dados transformados sejam pelos scritps ou pelos notebooks da pesquisa.
      - `rq0X/`: Diretórios reservados para cada questão de pesquisa.
      - ...

- Estrutura atual:
  - `data/`:
    - `oldData/`: 
      - ... (Demais arquivos da estrutura geral)
    - `newData/`:
      - ... (Demais arquivos da estrutura geral)

===========================================================
<!-- Rascunho -->

- `data/`: Centraliza todos os arquivos de dados a serem analisados do projeto.
    - `input_data/`: Dados brutos de entrada, intocáveis (JSON do SEART).
    - `analysis_data/`: Dados transformados pelos scripts (destino atual da Etapa 1; em migração — coletas antigas ainda estão em `output_rankings/`).
  
    - `context_detection/`: Resultados da Etapa 2 (CSV com detecção binária de arquivos).
    - `content_analysis/`: Resultados de extração de estrutura e classificação de cabeçalhos.
    - `testing_analysis/`: Dados extraídos para validação de fidelidade de testes.
- `scripts/`: Contém a lógica central de processamento.
    - `ranking/ranking.py`, `ranking/run_ranking.py`: Motor e script de entrada da Etapa 1 (módulo Python — ver instruções de execução abaixo).
    - `detect_ai_context_files/detect_via_api.py`, `detect_ai_context_files/detect_via_clone.py`, `detect_ai_context_files/run_detect_context.py`: Motor e script de entrada da Etapa 2 (módulo Python — ver instruções de execução abaixo).
- `notebooks/`: Análise visual e estatística dos dados.

===========================================================

## Stack Tecnológica (Tech Stack)
- **Linguagem:** Python 3.14
- **Bibliotecas Principais:** Pandas 3.0.2, NumPy 2.4.4, Requests 2.33.1, python-dotenv 1.2.2.
- **Visualização:** Matplotlib 3.10.9, Seaborn 0.13.2, Jupyter 1.1.1.
- Versões fixadas em `requirements.txt` (via `pip freeze`) para garantir reprodutibilidade.

## Configuração e Instalação (Setup)

> Todos os comandos abaixo devem ser executados a partir da **raiz do repositório**.

1. Criar ambiente virtual: `python -m venv .venv`
2. Ativar ambiente: `source .venv/bin/activate`
3. Instalar dependências: `pip install -r requirements.txt`
4. Configurar `.env`: criar um arquivo `.env` na raiz do projeto com `GITHUB_TOKEN=seu_token` e `GEMINI_API_KEY=seu_token`.
   
## Fluxo de Trabalho (Workflow)
O processo deve seguir rigorosamente estas etapas:

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

3. **Análise de Conteúdo e Fidelidade (Etapa 3):**
   - **Objetivo:** Extrair estrutura, classificar e validar o conteúdo dos arquivos detectados.
   - **Scripts:** `extract_content_structure.py`, `classify_headings.py`, `extract_testing_details.py`.
   - **Saídas:** Alocadas em `data/content_analysis/` e `data/testing_analysis/`.

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

### Etapa 3: Análise e Visualização

Nesta etapa, utilizamos os notebooks para transformar os dados coletados em gráficos e insights.

Como usar:
1. Com o ambiente virtual ativo, execute: jupyter notebook
2. Abra a pasta notebooks/ e escolha um dos arquivos:
  - analysis_data.ipynb: Gera gráficos de distribuição e adesão para uma única coleta de dados.
  - analysis_comparison.ipynb: Compara resultados de datas diferentes para mostrar a evolução temporal da adesão.

## Uso do Token do GitHub

Para evitar bloqueios por excesso de acessos na API do GitHub, você deve:
1. Criar um arquivo chamado .env na raiz do projeto.
2. Escrever dentro dele: GITHUB_TOKEN=seu_token_aqui

## Como Citar

Este repositório é licenciado sob os termos do arquivo [`LICENSE`](./LICENSE) (MIT). Para citar este trabalho, utilize as informações do arquivo [`CITATION.cff`](./CITATION.cff) ou a referência abaixo:

> SANTOS, Keven Alex Barbosa. **Engenharia de Contexto para Agentes de IA: Adoção, Sobreposição e Estrutura de Arquivos de Contexto em Repositórios de Código Aberto**. Universidade Federal de Campina Grande, 2026. Disponível em: https://github.com/kevenalex/tcc. DOI: [10.5281/zenodo.21388606](https://doi.org/10.5281/zenodo.21388606).

---
