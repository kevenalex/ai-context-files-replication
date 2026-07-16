# Detecção de Arquivos de Contexto

## Contexto
Contém os resultados da busca binária por arquivos de configuração de agentes de IA nos repositórios ranqueados. A detecção pode ser feita via **API** (mais rápida) ou **CLONE** (mais profunda).

## Esqueleto dos Dados (CSV)
O arquivo lista os repositórios e marca a presença (1) ou ausência (0) dos seguintes arquivos:
- `AGENTS.md`
- `CLAUDE.md`
- `COPILOT` (e variações de configuração)
- `GEMINI.md`
- `CURSOR` (e variações de configuração)

## Uso
Consumido por `scripts/extract_content_structure.py` e `scripts/download_ai_context_files.py` (Etapa 3) para selecionar quais repositórios/arquivos buscar, e pelo notebook `3-context-ai-repo-study.ipynb` para a análise de adesão.
