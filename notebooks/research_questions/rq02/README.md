# RQ02: Sobreposição Lexical e Semântica em Múltiplos Arquivos de Contexto de IA

## Questão de Pesquisa (RQ2)
Qual é o grau de sobreposição lexical e semântica de diretrizes em repositórios de código aberto que mantêm múltiplos arquivos de contexto para diferentes agentes de IA?

## Hipótese (H1)
Repositórios com múltiplos arquivos de contexto de IA apresentam alta redundância lexical e semântica. Essa multiplicidade não reflete uma especialização de regras por ferramenta, mas sim a ausência de padronização nos projetos de software, resultando em duplicação direta do esforço de manutenção da documentação.

## Objetivos
1. **Mapear a Coexistência:** Identificar a frequência de múltiplos arquivos de contexto em projetos de alta maturidade (Top 10k GitHub).
2. **Medir Sobreposição Lexical:** Calcular a similaridade de texto bruto entre arquivos de um mesmo repositório (ex: `.cursorrules` vs `CLAUDE.md`).
3. **Avaliar Sobreposição Semântica:** Utilizar LLMs para categorizar a relação entre instruções (Redundantes, Complementares ou Conflitantes).
4. **Analisar Esforço de Manutenção:** Discutir como a falta de padrões (ex: AGENTS.md, CLAUDE.md, GEMINI.md) impacta a evolução do projeto.

## Instruções para o Agente
- Utilize os dados de saída de `data/oldData/rq01/ai_context_files_in_repositories/` como base inicial.
- Foque na extração de amostras de conteúdo para comparação qualitativa.
- Documente cada descoberta relevante no notebook desta pasta.

## Referências
- `data/oldData/rq01/ai_context_files_in_repositories/context_api_top10000_24-08-2025_20260507_070457.csv` (Base de detecção principal)
- `data/oldData/rq02/semantic_analysis_rq01.csv` (Resultados da análise via LLM)
- `notebooks/3-context-ai-repo-study.ipynb` (Análise preliminar de adesão)
