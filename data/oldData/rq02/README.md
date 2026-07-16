# RQ2 — Sobreposição Lexical e Semântica em Múltiplos Arquivos de Contexto de IA

## Contexto
Esta pasta reúne os dados da RQ2 do artigo ("Qual é o grau de sobreposição lexical e semântica de diretrizes em repositórios de código aberto que mantêm múltiplos arquivos de contexto para diferentes agentes de IA?"): a análise semântica via LLM entre pares de arquivos do mesmo repositório, a amostragem estatística para revisão manual e os artefatos usados nessa revisão.

## Arquivos

1. **`semantic_analysis_rq01.csv`**: Resultado da comparação par-a-par (`file1`/`file2`) de cada repositório com múltiplos arquivos de contexto, gerado via LLM (Gemini) a partir do notebook `notebooks/research_questions/rq02/notebook.ipynb`.
   - Colunas: `analise_dimensional` (overlap de regras, especialização, risco de conflito), `similaridade_semantica` (0-100), `classificacao` (`Redundantes`/`Complementares`/`Conflitantes`), `detalhes_criticos`, `justificativa_final`, `repo`, `file1`, `file2`.
   - Prompt utilizado (LLM: Gemini 3.5 Flash, nível de raciocínio padrão):
     ```
     "Vou fornecer links de repositórios do GitHub. Para cada link, crie um resumo em texto corrido de, no máximo, 25 palavras. O texto deve ser uma única frase fluida e direta que conecte o que é o software, qual problema ele resolve (objetivo) e quem é o seu público-alvo ou caso de uso. Não use tópicos ou quebras de linha."
     ```
2. **`sample.csv`**: Amostra de repositórios sorteada por `scripts/sample_manual_validation.py` a partir do arquivo acima, usando a fórmula de Cochran (com correção para população finita) para garantir significância estatística.
3. **`sample_to_manual_review_24-06-2026.csv`** / **`manual_review_sample_to_manual_of_review_24-06-2026.csv`**: Planilhas "cegas" (sem a classificação automática do LLM) com links diretos para os arquivos de cada repositório amostrado, geradas por `scripts/build_manual_review_sheet.py` para revisão manual. As colunas `classificacao_manual`/`evidencia_manual` ficam vazias nestes arquivos de propósito — o preenchimento real da revisão manual é feito à parte (ver nota abaixo).
4. **`repo_checklist.csv`**: Checklist por repositório (agrupando os pares de arquivo a revisar de um mesmo repositório), gerado por `scripts/build_repo_checklist.py` a partir do arquivo de amostra com links.

> **Nota:** a planilha com a revisão manual efetivamente preenchida é mantida à parte deste repositório e está publicada, junto com os dados brutos do SEART, no Zenodo: [10.5281/zenodo.21388606](https://doi.org/10.5281/zenodo.21388606). O acesso aos arquivos é privado por decisão do autor; caso seja necessário, deve ser solicitado diretamente pela página do depósito.

## Uso
Consumido pelo notebook `notebooks/research_questions/rq02/notebook.ipynb`. Alimentado pelo pipeline de detecção/coleta de conteúdo da RQ1 (`data/oldData/rq01/`).
