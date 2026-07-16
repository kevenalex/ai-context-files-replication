# Checklist de Correções — Preparação para Etapa 3 (Reprodutibilidade)

Levantamento inicial feito em 2026-07-15. Em 2026-07-16, `data/` foi totalmente reorganizada: só existem `oldData/` e `newData/` no topo, cada uma com `input_data/` (só JSON bruto do SEART), `rq01/` (RQ1 do artigo — natureza temática das diretrizes, incluindo ranking/detecção/coleta bruta que alimentam essa RQ), `rq02/` (RQ2 do artigo — sobreposição lexical/semântica) e `misc/` (dados que não são de nenhuma RQ, ex: `testing_analysis/`). Todos os scripts, notebooks e READMEs afetados foram atualizados para os novos caminhos.

Marque cada item conforme for resolvido.

## 🔴 Crítico (quebra reprodutibilidade)

- [X] **`.gitignore` com exceção morta.** A regra `!data/input_data/*-seart_data_sample.json` (linha 15) não bate com a estrutura atual (`data/newData/input_data/`). O único JSON de amostra pensado para ser público (`06-16-2026-seart_data_sample.json`) continua sendo **ignorado pelo git**.
- [ ] **Toda a árvore `data/oldData/` e `data/newData/` está não rastreada pelo git** (`??` no `git status`). Nada foi commitado ainda, incluindo os 1829 arquivos de contexto coletados em `rq01/rq00/`. Resolver (add/commit) depois de corrigir o `.gitignore` (item acima).
- [ ] **`CITATION` e `LICENSE` vazios (0 bytes).** Sem license, o repositório público é "todos os direitos reservados" por padrão — impede reuso por terceiros, contra o requisito de ciência aberta da Etapa 3.

## 🟡 Médio (documentação desatualizada/inconsistente)

- [ ] `data/oldData/rq02/README.md` só tem o prompt usado, sem contexto/estrutura (inconsistente com o padrão dos outros READMEs de dados — comparar com `data/oldData/rq01/README.md`, já reescrito).
- [ ] `README.md` raiz: bloco `<!-- Rascunho -->` duplicado na seção "Estrutura do repositório" (ainda descreve a estrutura antiga de `data/`, não a atual `oldData/rq01/rq02/misc`).
- [ ] `README.md` raiz: Etapa 3 do Workflow ainda descrita de duas formas conflitantes (scripts de conteúdo vs. notebooks de visualização com nomes que não existem).
- [ ] 5 scripts sem nenhuma menção no Workflow do README: `build_manual_review_sheet.py`, `build_repo_checklist.py`, `download_ai_context_files.py`, `regex_analysis_content.py`, `sample_manual_validation.py`.
- [ ] A pasta `notebooks/research_questions/rq01/` estuda, na verdade, a **RQ2** do artigo (sobreposição lexical/semântica) — o número da pasta ficou invertido em relação à nomenclatura final do artigo. Decidir se vale renomear para `rq02/` (fora do escopo desta rodada de correções).

## 🟢 Organização (nice-to-have)

- [ ] `test/` contém 2 notebooks (não testes automatizados) — `test/analysis_comparison.ipynb` diverge do homônimo em `notebooks/` (hash diferente), parece rascunho esquecido.
- [ ] `notebooks/analysis_comparison.ipynb` não está na numeração 1-7, parece avulso.
- [ ] `results/` só tem um PDF compilado, ainda não versionado — decidir se deve entrar no git.
- [ ] `docs/` só tem este checklist — ok se não for necessário mais nada.

## Já corrigido

**Sessão 2026-07-15:**
- [x] `requirements.txt` e seção "Stack Tecnológica" do README: versões fixadas (`==`) e Python especificado como 3.14.
- [x] Seção "Configuração e Instalação" do README: explicitado que os comandos rodam a partir da raiz do repositório.

**Sessão 2026-07-16 — reorganização de `data/` por RQ:**
- [x] `data/` reestruturada: `oldData/`/`newData/`, cada uma com `input_data/`, `rq01/` (ranking, detecção, `rq00/` bruto, `structure_analysis*.csv`), `rq02/` (amostra de revisão manual, `semantic_analysis_rq01.csv`) e `misc/testing_analysis/`.
- [x] Confirmado que nenhum dado foi perdido na migração (contagem de arquivos batendo em todas as pastas antes/depois).
- [x] 10 scripts atualizados para os novos caminhos: `ranking/run_ranking.py`, `detect_ai_context_files/run_detect_context.py`, `extract_content_structure.py`, `classify_headings.py`, `extract_testing_details.py`, `sample_manual_validation.py`, `build_manual_review_sheet.py`, `build_repo_checklist.py`, `regex_analysis_content.py`, `download_ai_context_files.py`.
- [x] 9 notebooks atualizados: `2-ranking_data_study.ipynb`, `analysis_comparison.ipynb`, `3-context-ai-repo-study.ipynb`, `4-structure_analysis_study.ipynb`, `5-ai-file-classification-study.ipynb`, `6.1-test-validity-checker.ipynb`, `7-repo_level_category_study.ipynb`, `research_questions/rq01/notebook.ipynb`, `test/analysis_content_structure.ipynb`.
- [x] Verificado que todos os `INPUT`/`INPUT_CSV`/`INPUT_FILE` hardcoded apontam para arquivos que realmente existem no disco (checagem `test -f` em 10 caminhos-chave).
- [x] `data/oldData/rq01/README.md` (antigo `data/content_analysis/README.md`) reescrito para descrever todo o conteúdo real da pasta e preencher a seção "Uso".
- [x] `data/oldData/rq01/ai_context_files_in_repositories/README.md`: seção "Uso" preenchida.
- [x] `notebooks/research_questions/rq01/README.md`: referências a `data/context_detection/` e `data/content_analysis/` corrigidas para os caminhos novos.
- [x] `registro.md`: referências a `data/context_detection/` e `data/seart_data/` corrigidas.
- [x] `data/newData/input_data/README.md`: referência a `scripts/run_ranking.py` corrigida para `scripts/ranking/run_ranking.py`.
