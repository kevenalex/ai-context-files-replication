# Contexto para Agentes de IA - Projeto de Pesquisa

Este arquivo fornece um registro das atividades já realizas e que estão pendentes nesta pesquisa.

Quaisquer instruções sobre aspectos de execução dos scripts deste projeto estaram listadas no arquivo README.md, na raíz deste projeto.


## Objetivos do Projeto (Goals/Purposes)
O objetivo principal é coletar, processar e analisar a presença de arquivos de contexto de IA (como `AGENTS.md`, `CLAUDE.md`, etc.) em repositórios populares do GitHub, visando entender a adoção e evolução dessa prática.

## Materiais de Referência (Reference Materials)
O diretório `scripts-referencia/` é dedicado ao armazenamento de materiais externos, códigos de terceiros, artigos e qualquer recurso que sirva de base ou inspiração para o crescimento desta pesquisa.

- **Propósito:** Servir como base de conhecimento e "Gold Standard" para validação das metodologias implementadas neste repositório.
- **Conteúdo Atual:** Inclui o material suplementar original (scripts de coleta, análise e dados brutos) do artigo *"Context Engineering for AI Agents in Open-Source Software"*.
- **Expansibilidade:** Este espaço deve ser utilizado para novos artigos e ferramentas que venham a ser incorporados ao escopo do TCC.

## Status da Pesquisa (Current Status)

### O que já foi realizado (Done)
- **Infraestrutura de Detecção:** Scripts para detecção binária (existe/não existe) arquivos AGENTS.md via API e Clone concluídos.
- **Ranqueamento de Repositórios:** Algoritmo de classificação por maturidade e popularidade operacional.
- **Coleta de Snapshots:** Dados coletados para três períodos (Ago/2025, Mar/2026, Abr/2026).
- **Análise de Adesão (RQ1):** Notebooks para medir a porcentagem de adoção (`3-context-ai-repo-study.ipynb`) e comparação temporal concluídos.
- **Análise de Conteúdo (RQ2):** Script de extração de estrutura (`extract_content_structure.py`) e notebook de visualização (`analysis_content_structure.ipynb`) concluídos.
- **Estudos de Dados:** Notebooks para estudo dos dados brutos do SEART (`1-seart_data_study.ipynb`), dados ranqueados (`2-ranking_data_study.ipynb`), detecção de contexto (`3-context-ai-repo-study.ipynb`) e classificação de conteúdo (`4-ai-file-classification-study.ipynb`) concluídos.
- **Reorganização de Dados:** Centralização de arquivos de dados na pasta `data/` com subpastas categorizadas por etapa da pesquisa.

### Em Andamento (In Progress)
- **Aumento de Amostragem:** Transição de testes com 100 repositórios para o Top 10.000.
- **RQ01 - Padrões de Múltiplos Arquivos:** Estudo sobre projetos com 2+ arquivos de contexto.
  - Path: `notebooks/research_questions/rq01/`

### Próximos Passos (To Do / Roadmap)
1. **Análise de Evolução Histórica (RQ3):**
   - Implementar rastreamento de commits para arquivos de contexto.
   - Analisar frequência e tipos de mudanças (ref. Tabela 2 do artigo).
2. **Validação Estatística:**
   - Correlacionar a presença de arquivos de contexto com o tamanho do projeto e linguagem de programação.

## Diretrizes e Convenções para agentes de IA

- **Organização de Questões de Pesquisa (RQs):** Cada nova questão de pesquisa deve possuir sua própria pasta em `notebooks/research_questions/RQ_NAME/`. Esta pasta deve conter obrigatoriamente:
    - `README.md`: Documentando o contexto, objetivos específicos e instruções para o agente conduzir aquela pesquisa.
    - `notebook.ipynb`: O arquivo de execução e análise daquela RQ.
- **Gerenciamento de Dados:** Todos os dados gerados ou consumidos devem estar na pasta `data/`, sempre dentro de `oldData/` ou `newData/` conforme a coleta, organizados por sub-pasta de RQ (ex: `data/oldData/rq01/`). Nunca utilize pastas temporárias ou de saída na raiz.
- **Modo de Operação:** Ao modificar scripts de execução (`run_*.py`), mantenha a estrutura de variáveis clara para facilitar a replicabilidade.
- **Segurança:** Nunca exponha o `GITHUB_TOKEN`. Sempre verifique se o `.env` está no `.gitignore`.
- **Tratamento de Dados:** Use Pandas para manipulação de grandes volumes de dados. Garanta que os caminhos de entrada e saída nos scripts de execução estejam corretos antes de rodar.
- **Estilo de Resposta:** Seja prescritivo e direto. Ao sugerir mudanças, foque na eficiência do processamento de dados.

## Segurança e Eficiência de Tokens (Efficiency & Safety)
- **Arquivos Massivos:** Arquivos JSON em `data/oldData/input_data/` e `data/newData/input_data/` superam 300MB. 
   - **REGRA DE OURO:** NUNCA peça para a IA ler o arquivo completo (`read_file`). Isso causará erro de limite de tokens e desperdício de processamento.
   - **COMO AGIR:** Utilize sempre amostragem (ex: `load_sample_json`) ou inspeção de metadados (`head`, `tail`, `grep`).
- **Contexto de Conversa:** Para evitar o estouro da janela de contexto da IA, prefira processar dados e gerar resumos (CSVs menores) em vez de manter grandes estruturas de dados na memória do agente.
- **Segurança de Credenciais:** O arquivo `.env` contém o `GITHUB_TOKEN`. Nunca imprima seu conteúdo ou o inclua em commits/logs.

## Referências
- Artigo base: "Context Engineering for AI Agents in Open-Source Software".
- Documentação do SEART para coleta de dados brutos.
