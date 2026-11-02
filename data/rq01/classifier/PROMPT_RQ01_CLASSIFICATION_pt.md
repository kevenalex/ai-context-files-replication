# Classificação de conteúdo de arquivos de contexto de IA (RQ1)

Execução em lote com o Claude Code, a partir da raiz do repositório `repo-pesquisa`. Este prompt é autossuficiente: as regras de classificação estão todas abaixo (Parte A) e o procedimento de execução vem em seguida (Parte B).

## Objetivo

Classificar o conteúdo de cada arquivo de contexto de IA (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md`, `.cursorrules`) em 13 categorias fechadas. A população é de 1.828 arquivos. Cada sessão processa um lote de 30 arquivos e para; uma nova sessão com este mesmo prompt continua de onde a anterior parou.

A classificação é repetida em execuções independentes (`EXECUCAO` = 1, 2 ou 3) para medir a variabilidade do modelo. Por isso, cada execução grava em um arquivo próprio e não pode depender das outras.

---

# Parte A — Regras de classificação

## A1. Papel

Você é um pesquisador auditando arquivos de contexto de IA de repositórios open-source. Para cada arquivo, identifique **quais das 13 categorias de conteúdo (seção A5) estão presentes no texto**, com a evidência literal que justifica cada uma.

## A2. Regra de escopo

**Avalie apenas o conteúdo do próprio arquivo.** Se o arquivo referenciar ou apontar para outro arquivo (ex.: `@AGENTS.md`, "See CLAUDE.md for details", um link para `docs/ai/README.md`), **não explore o conteúdo do arquivo referenciado**. A referência em si conta como conteúdo (normalmente `doc_metadata`), mas o que está dentro do arquivo apontado não é considerado.

Exemplo âncora: um `CLAUDE.md` cujo conteúdo inteiro é a linha `@AGENTS.md` (import puro, sintaxe do Claude Code) deve ser classificado **somente** com `doc_metadata`, mesmo que o `AGENTS.md` referenciado seja extenso e cubra várias outras categorias.

## A3. Procedimento por arquivo

1. Leia o arquivo **por completo**, do início ao fim, nunca só os títulos ou o índice. Categorias relevantes frequentemente aparecem no meio ou no fim do arquivo.
2. Para cada uma das 13 categorias (seção A5), pergunte: *este arquivo contém uma passagem que se encaixa na definição desta categoria?*
3. Se sim, marque a categoria como presente e registre a evidência (seção A6).
4. Ao final, revise: você releu o arquivo inteiro ou só a parte de cima? Se pulou alguma seção, volte e releia antes de finalizar.

## A4. Multirrótulo e desambiguação

As categorias **não são mutuamente exclusivas**: uma mesma passagem pode justificar mais de uma categoria. Na dúvida real entre duas categorias vizinhas, **marque as duas**; o risco de perder uma categoria genuinamente presente é maior que o de marcar uma a mais.

Pares que mais geram confusão, com a regra de desempate:

- **`ai_rules` vs. `code_conventions`**: regra sobre *como escrever código* (sintaxe, formatação, nomenclatura) é `code_conventions`. Regra sobre *como o agente de IA deve se comportar* (mesmo que o resultado seja código) é `ai_rules`. Ex.: "marque blocos de código gerados por IA com um comentário `// AI:`" é `ai_rules`, não `code_conventions`.
- **`security` vs. `code_conventions`**: uma regra como "nunca hardcode secrets" é `security`, mesmo fraseada como prática de codificação.
- **`run_and_build` vs. `test_instructions`**: comando cujo propósito é rodar ou validar testes é `test_instructions`; comando de build ou instalação genérico é `run_and_build`.
- **`project_overview` vs. `system_design`**: o overview descreve *o que* é o projeto; `system_design` descreve *como* ele é internamente estruturado (padrões, decisões de arquitetura).
- **`performance_&_resource_management` vs. `ai_rules`** *(par exclusivo: escolha um)*: desempenho ou consumo de recursos do **software sendo desenvolvido** (latência, memória, I/O, benchmarks) é `performance_&_resource_management`. Preocupação com o custo ou consumo de **tokens do próprio agente** ao executar a tarefa (ex.: "evite re-derivar informação determinística a cada execução para não gastar tokens à toa") é sobre o comportamento do agente: marque `ai_rules`, não `performance_&_resource_management`.
- **`system_design` vs. `ai_rules`** *(par exclusivo: escolha um)*: uma passagem que **descreve** a arquitetura ou os padrões do sistema (fluxo de dados, camadas, padrões de projeto) é `system_design`. Uma passagem que **instrui o comportamento do agente** ao mexer nessa arquitetura (ex.: "não alucine formatos de AST, verifique identificadores antes de usá-los") é `ai_rules`, mesmo que mencione componentes internos do sistema.
- **`contribution_guidelines` vs. `ai_rules`** *(par aditivo: marque as duas quando for o caso)*: processo de PR ou commit que vale para qualquer contribuidor (humano ou IA) é `contribution_guidelines`. Regra que só faz sentido para um agente de IA (ex.: "IAs devem se identificar como tal na descrição do PR") é **também** `ai_rules`, sem remover `contribution_guidelines`.

> **Importante:** só os dois pares marcados como *exclusivos* funcionam no modelo "ou um ou outro". Todos os demais pares, incluindo `contribution_guidelines` vs. `ai_rules`, são **aditivos**: o fato de um trecho se qualificar como `ai_rules` não é motivo para remover ou deixar de marcar outra categoria que também se aplique. Não generalize o padrão "escolha um" para outros pares. Trate cada categoria da seção A5 como uma pergunta independente (passo 2 da seção A3).

## A5. Vocabulário das 13 categorias

| Categoria | Definição | Exemplo âncora |
|---|---|---|
| `run_and_build` | Instruções de build da aplicação; gerenciamento de dependências; instruções sobre como executar a aplicação. | `"Run pnpm build to build all packages"; "Run pnpm install to install dependencies"` |
| `project_overview` | Descrição da ferramenta; contextualização do uso do repositório; principais ferramentas, linguagens e dependências que o software utiliza. | `"Project Overview — Vitest is a next-generation testing framework powered by Vite..."` |
| `doc_metadata` | Documentações latentes a especificações de código; referências para **outros** arquivos ou pastas de documentação (incluindo outros arquivos de contexto de IA). **Não conta** a frase padrão de autodescrição do próprio arquivo (ex.: "This file provides guidance to Claude Code when working with code in this repository"), que é só o cabeçalho introdutório. | `"Essential references — Agent-specific guide: See AGENTS.md"` |
| `test_instructions` | Como criar testes; funcionamento dos testes no projeto; localização dos testes na estrutura de arquivos; como executar testes. | `"pnpm test packages/react-router/__tests__/router/fetchers-test.ts  # Single file"` |
| `project_structure` | Organização física dos arquivos e diretórios do repositório. | `"Project Structure — kotest-common/  # Shared annotations..."` |
| `system_design` | Padrões do projeto; design patterns e afins (arquitetura interna). | `"Follow ChurchCRM patterns: Use Perpl ORM (never raw SQL)..."` |
| `contribution_guidelines` | Padrões de branch e commit; processo de contribuição externa (CLA, templates de PR e issue, requisitos para aceite de PR). | `"All contributors must review the CLA and sign it by adding their github username to contributors.yml"` |
| `code_conventions` | Guias de sintaxe do código produzido; formatação; estilo de nomenclatura (camelCase, PascalCase etc.). | `"Do not add one-line comments unless you think they are really useful"` |
| `ai_rules` | Instrução projetada exclusivamente para a LLM: não fala da lógica do sistema, mas de como a LLM deve atuar em cenários específicos. | `"AI-generated source code blocks must be marked with // AI: below section was generated by an AI"` |
| `performance_&_resource_management` | Custos de execução de pipelines; restrições de uso ou implementação por aspecto de hardware; otimizações. | `"This is a performance-critical testing framework — Pay attention to import costs and bundle size"` |
| `troubleshooting` | Soluções de problemas comuns da aplicação ou das ferramentas usadas pelo sistema. | `"Ensure pnpm is used (not npm/yarn); Build before running tests"` |
| `security` | Autenticação, autorização e controle de acesso; validação de entrada e proteção contra vulnerabilidades comuns; tratamento de dados sensíveis; política de divulgação de vulnerabilidades. | `"Security first: Check authorization, input validation, and data sensitivity for every change"` |
| `deployment_&_infrastructure` | Especificações de CI e CD; especificações de deploy. Precisa ser uma **instrução ou especificação real** (pipeline, comando, processo). **Não conta** uma menção passageira de onde a aplicação roda em produção (ex.: "the system runs in Kubernetes in production") sem detalhar o processo; isso é `project_overview` ou `system_design`. | `"Push to main triggers .github/workflows/server-production-deployment.yml, which cascades canary → acceptance tests → production"` |

## A6. Regra de evidência

Toda categoria marcada como presente precisa de uma evidência **literal** (citação direta do texto, não paráfrase). Se a categoria aparece em mais de um trecho, **una os trechos em uma só célula, de forma concisa**: trechos curtos separados por ` [...] `, nunca o parágrafo inteiro colado. O alvo é de 3 a 5 linhas de evidência por categoria.

## A7. Casos-limite

- **Arquivo-ponteiro puro** (`@AGENTS.md`, "See CLAUDE.md for complete instructions"): recebe só `doc_metadata` (seção A2). É o resultado esperado, não um erro.
- **Conteúdo genérico, não relacionado ao repositório** (ex.: um `CLAUDE.md` que só descreve como o Claude Code deve paralelizar suas tarefas, sem nada específico do projeto): classifique pelo que de fato contém (tipicamente `ai_rules`), mesmo que não seja conteúdo útil ou específico.

## A8. Na dúvida

Se, depois de aplicar as regras de desambiguação (seção A4), ainda houver incerteza genuína sobre uma categoria, prefira marcá-la como presente com uma evidência mais fraca a deixá-la de fora, mas nunca marque uma categoria sem alguma citação literal que a sustente. Nunca infira uma categoria pela ausência de conteúdo (ex.: não marque `security` só porque o projeto parece lidar com dados sensíveis); a categoria precisa de uma passagem real no texto.

---

# Parte B — Execução

## B1. Parâmetros

- `EXECUCAO`: identificador da execução (1, 2 ou 3; `sample` ou `validation` na reprodução por amostra), informado na mesma mensagem que este prompt. Se não foi informado, pare e pergunte.
- `MANIFESTO`: lista de arquivos a classificar. Se não for informado, use `data/collection/context_files/download_manifest.csv`.
- `PASTA_SAIDA`: pasta dos arquivos de saída. Se não for informada, use `data/rq01/classifier`.
- Arquivo de saída: `<PASTA_SAIDA>/rq01_classification_run_<EXECUCAO>.csv`
- Arquivo de registro: `<PASTA_SAIDA>/rq01_run_<EXECUCAO>_log.csv`, com as colunas `lote_inicio`, `lote_fim`, `arquivos`, `modelo`, `data_hora_utc`.

## B2. Regras de independência

- Leia apenas este prompt, a lista de arquivos baixados (`download_manifest.csv`, ver seção B3), os arquivos a classificar e o arquivo de saída desta execução. Não abra outros arquivos do repositório (em especial rótulos manuais, classificações anteriores, saídas de outras execuções e o roteiro antigo da RQ1), para que a classificação não seja influenciada por rótulos já existentes.
- Classifique cada arquivo apenas pelo que está escrito nele e pelas regras da Parte A. Não use conhecimento externo sobre o repositório.
- Não reclassifique um par `(repo, arquivo_analisado)` que já esteja no arquivo de saída desta execução.

## B3. Identifique os arquivos pendentes

1. Leia o `MANIFESTO` (colunas `repo`, `file_label`, `local_path`, `status`) e mantenha só as linhas com `status == "ok"`. No manifesto completo são 1.828 arquivos. O caminho do arquivo é montado como em B4.
2. Se o arquivo de saída desta execução existir, leia os pares `(repo, arquivo_analisado)` já presentes nele. Se não existir, crie a `PASTA_SAIDA` e o arquivo com o cabeçalho de B5.
3. Os pendentes são as linhas do manifest cujo par `(repo, file_label)` não está no arquivo de saída, na ordem do manifest.
4. Informe quantos arquivos já foram classificados e quantos faltam (por exemplo, "347/1828 feitos, 1481 pendentes").

## B4. Classifique um lote

Pegue os próximos 30 arquivos pendentes. Para cada um:

1. Localize o arquivo em `data/collection/context_files/<repo com "/" trocado por "__">/<nome_local>`, onde `nome_local` depende do `file_label`:

   | `file_label` | `nome_local` |
   |---|---|
   | `AGENTS.md` | `AGENTS.md` |
   | `CLAUDE.md` | `CLAUDE.md` |
   | `COPILOT` | `copilot-instructions.md` |
   | `CURSOR` | `.cursorrules` |
   | `GEMINI.md` | `GEMINI.md` |

   Exemplo: `elastic/elasticsearch` com `AGENTS.md` está em `data/collection/context_files/elastic__elasticsearch/AGENTS.md`.

2. Classifique o arquivo seguindo a Parte A (procedimento da seção A3). A classificação é feita por você, lendo e interpretando o texto: não use scripts, expressões regulares ou busca por palavras-chave para atribuir categorias, e não delegue a classificação a subagentes. Scripts servem só para listar pendentes, gravar e verificar o CSV.
3. Só use a coluna `erro` quando o arquivo não puder ser lido; nesse caso, descreva o problema em poucas palavras e deixe as colunas de categoria vazias. Arquivos vazios ou ponteiros puros não são erro: siga a seção A7.

## B5. Grave o resultado

Anexe uma linha por arquivo ao final do arquivo de saída. Nunca reescreva o arquivo inteiro. Grave com o módulo `csv` do Python (`csv.writer`, UTF-8, `newline=""`), nunca montando linhas por concatenação de texto, porque as evidências contêm vírgulas, aspas e quebras de linha.

Colunas, nesta ordem exata:

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

- `repo`: valor de `repo` no manifest.
- `arquivo_analisado`: valor de `file_label` no manifest.
- `link_arquivo`: `local:<caminho do arquivo, relativo à raiz do repositório>`.
- Colunas de categoria: `1` ou `0`.
- Colunas de evidência: citação literal (seção A6) se a categoria estiver presente; vazio se estiver ausente.
- `erro`: vazio, salvo no caso descrito em B4.

Depois de gravar, anexe uma linha ao arquivo de registro com o primeiro e o último arquivo do lote, a quantidade de arquivos, o identificador do modelo desta sessão e a data e hora em UTC.

## B6. Verifique o lote

Antes de encerrar, confira com um script as linhas que acabou de gravar:

- cada linha tem exatamente 30 colunas (3 de identificação, 26 de categoria e evidência, e `erro`);
- as colunas de categoria contêm só `0` e `1`;
- toda categoria `1` tem evidência e toda categoria `0` tem evidência vazia;
- não há pares `(repo, arquivo_analisado)` duplicados no arquivo de saída.

Corrija qualquer inconsistência antes de seguir.

## B7. Relate e siga

Informe quantos arquivos foram classificados nesta sessão, quantos faltam no total e se algum arquivo deu erro (e qual). Rode o prompt novamente para o próximo lote
