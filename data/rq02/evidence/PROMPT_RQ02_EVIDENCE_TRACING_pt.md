# Prompt de lote — Rastreio das evidências da RQ2 e cruzamento com as categorias da RQ1

**Como usar:** cole este arquivo inteiro como primeira mensagem de uma sessão do Claude Code, a partir
da raiz do repositório, informando os parâmetros abaixo na mesma mensagem. Cada sessão processa um
lote e para. Rode o mesmo prompt de novo, em sessão nova, para continuar de onde parou.

**Parâmetros**

- `ENTRADA`: rótulos e evidências da anotação manual, um repositório por linha. Se não for informada,
  use `data/rq02/manual_annotation/rq02_labels_annotator_A.csv`.
- `PASTA_SAIDA`: pasta das saídas. Se não for informada, use `data/rq02/evidence`.
- Saída por repositório: `<PASTA_SAIDA>/rq02_evidence.csv`; saída longa: `<PASTA_SAIDA>/rq02_evidence_items.csv`.

---

## Contexto (leia antes de agir)

A RQ2 classifica a relação entre os arquivos de contexto de IA de um mesmo repositório
(`conflitantes`, `redundantes`, `complementares`). A anotação manual já decidiu, para cada repositório
da `ENTRADA`, se cada relação existe (0/1) e registrou as evidências em texto livre.

**Sua tarefa não é reclassificar.** É rastrear: pegar cada evidência registrada pelo anotador, achar
nos arquivos de origem os trechos exatos a que ela se refere, separar em itens atômicos, contar, e
dizer a qual categoria de conteúdo da RQ01 cada item pertence. O objetivo final é uma matriz
categoria RQ01 × relação RQ02 (ex.: "conflitos acontecem mais em `run_and_build`; redundâncias,
em `test_instructions`").

## Passo 1 — Leia as definições

1. `data/rq01/classifier/PROMPT_RQ01_CLASSIFICATION_pt.md`, seções A4 e A5 da Parte A por
   inteiro: as 13 categorias e as regras de desambiguação. Use exatamente esses nomes:
   `run_and_build`, `project_overview`, `doc_metadata`, `test_instructions`, `project_structure`,
   `system_design`, `contribution_guidelines`, `code_conventions`, `ai_rules`,
   `performance_&_resource_management`, `troubleshooting`, `security`,
   `deployment_&_infrastructure`.
2. As três relações e os critérios de fronteira usados na anotação:
   - `complementares`: os arquivos trazem informações distintas que, juntas, enriquecem o contexto do agente.
   - `redundantes`: a mesma informação se repete em dois ou mais arquivos, mesmo com outras palavras.
   - `conflitantes`: os arquivos dão instruções contraditórias sobre o mesmo aspecto do projeto.
   - Diferença só de escopo (o mesmo tópico para casos ou ferramentas diferentes) é `complementar`,
     não conflito.
   - Arquivo que apenas encaminha o agente para outro (ponteiro) é `complementar`. Uma referência
     cruzada sozinha não é `redundante`.
   - O mesmo fato dito duas vezes é `redundante`, qualquer que seja a redação.
   - Um valor diferente para o mesmo fato (versão, comando, nome) é `conflitante`.

## Passo 2 — Descubra o que falta fazer

1. Leia a `ENTRADA`. Colunas:
   `repo, status, qtd_arquivos, arquivos_para_analisar, links_arquivos, conflitantes,
   conflitantes_evidencia, conflitantes_evidencia_qnt, redundantes, redundantes_evidencia,
   redundantes_evidencia_qnt, complementares, complementares_evidencia,
   complementares_evidencia_qnt`.
2. Leia a saída por repositório (`<PASTA_SAIDA>/rq02_evidence.csv`). Se não existir, crie a
   `PASTA_SAIDA` e o arquivo com o cabeçalho do Passo 4. Os repositórios já presentes nela estão feitos.
3. Pendentes = linhas da entrada cujo `repo` ainda não está na saída, na ordem da entrada.
4. Imprima quantos estão feitos e quantos faltam (ex.: "12/47 feitos, 35 pendentes").

## Passo 3 — Rode um lote de 8 repositórios

Para cada repositório pendente:

### 3.1 Localize os arquivos

O nome do repositório vem da URL em `repo` (`https://github.com/<owner>/<nome>`, ignore o que vier
depois). A pasta é `data/collection/context_files/<owner>__<nome>/` (o caso das letras pode
diferir: procure sem diferenciar maiúsculas). O arquivo local depende do rótulo em
`arquivos_para_analisar`:

| rótulo | arquivo local |
|---|---|
| `AGENTS.md` | `AGENTS.md` |
| `CLAUDE.md` | `CLAUDE.md` |
| `COPILOT` | `copilot-instructions.md` |
| `CURSOR` | `.cursorrules` |
| `GEMINI.md` | `GEMINI.md` |

Leia **todos os arquivos por completo, com número de linha** (ex.: `cat -n`). Não trabalhe só com
busca por palavra-chave: a evidência do anotador costuma parafrasear.

### 3.2 Separe as evidências em itens atômicos

Para cada relação (`conflitantes`, `redundantes`, `complementares`) cuja coluna `_evidencia` não
está vazia:

- **Um item = uma unidade de informação** (um fato, uma regra, um comando, um tópico) envolvida
  naquela relação. Se o anotador juntou vários tópicos numa frase ("Mapa de módulos, spotless:apply,
  checkstyle:check, jacoco e -pl/-Dtest repetidos"), separe em um item por tópico (aqui, 5 itens).
  Se ele separou em bullets algo que é a mesma informação dita duas vezes, junte em um item.
- Não invente itens que o anotador não mencionou, mesmo que você veja outras sobreposições nos
  arquivos. Se notar algo relevante que ficou de fora, anote em `observacoes` (Passo 4), sem
  contar.
- Frases genéricas que apontam para um tópico sem detalhar ("diversos tópicos, ex.: Threading, são
  especificados de forma sobreposta") viram um item por tópico **que você conseguir localizar**
  nos arquivos a partir do exemplo dado. Não expanda para tópicos que o anotador não nomeou.

### 3.3 Localize cada item nos arquivos

Para cada item, encontre o(s) trecho(s) literal(is):

- `conflitantes` e `redundantes`: um trecho de **cada** arquivo envolvido no par.
- `complementares`: o trecho do arquivo que tem o conteúdo exclusivo (o outro arquivo não tem
  nada a citar), ou os dois trechos quando são descrições distintas do mesmo tópico. Para
  arquivo-ponteiro, cite a linha da delegação ("See AGENTS.md...").

Marque o status de cada item:

- `[OK]` — trechos encontrados e sustentam a relação.
- `[PARCIAL]` — o tópico existe nos arquivos, mas a evidência exagera ou não sustenta bem a
  relação (ex.: a evidência diz "se repete quase por inteiro" e só uma frase se repete; ou o "conflito"
  é de escopo e não de diretiva oposta). Diga em poucas palavras por quê.
- `[NAO_LOCALIZADO]` — o texto descrito não existe nos arquivos. Diga o que procurou.

### 3.4 Atribua a categoria da RQ01

Cada item recebe **uma categoria principal** da RQ01, a que melhor descreve o conteúdo dos trechos
(não o tipo de relação). Use as regras de desambiguação da seção A4 do prompt da RQ1 (ex.:
comando para rodar testes é `test_instructions`, não `run_and_build`; regra de comportamento do
agente é `ai_rules`). Exemplos:

- versões divergentes de pnpm entre arquivos → `run_and_build`
- prefixo `m_` vs `snake_case` sem prefixo → `code_conventions`
- "não mockar objetos simples" vs "default to mocks" → `test_instructions`
- arquivo-ponteiro que delega a outro arquivo → `doc_metadata`
- fluxo de PR com `gh pr create` → `contribution_guidelines`

Se o item cobrir genuinamente duas categorias, escolha a principal e cite a outra entre parênteses
como secundária. A contagem da matriz usa só a principal.

### 3.5 Formato de cada item

Um item por linha, começando com `- `:

```
- [OK] [run_and_build] versão do pnpm diverge — AGENTS.md l.14: "pnpm 10.26.2" | CLAUDE.md l.12: "pnpm v10.9.0"
- [OK] [doc_metadata] copilot delega ao AGENTS.md — copilot-instructions.md l.1: "See ../AGENTS.md for project-specific..."
- [PARCIAL] [project_overview] descrição do projeto "igual" — só a primeira frase coincide — CLAUDE.md l.3: "..." | copilot-instructions.md l.2: "..."
- [NAO_LOCALIZADO] [contribution_guidelines] "never rely on remote names or hard-code origin" — procurado em AGENTS.md e copilot-instructions.md, não existe
```

Trechos curtos: o suficiente para conferir, unidos por `[...]` se precisar. Nunca cole parágrafos.

## Passo 4 — Grave a saída

### 4.1 Saída por repositório: `<PASTA_SAIDA>/rq02_evidence.csv`

Uma linha por repositório, com estas colunas, nesta ordem:

```
repo, arquivos_para_analisar,
conflitantes, conflitantes_evidencia_tratada, conflitantes_evidencia_qnt, conflitantes_categorias_rq01,
redundantes, redundantes_evidencia_tratada, redundantes_evidencia_qnt, redundantes_categorias_rq01,
complementares, complementares_evidencia_tratada, complementares_evidencia_qnt, complementares_categorias_rq01,
itens_parciais, itens_nao_localizados, observacoes
```

- `repo`, `arquivos_para_analisar` e os três 0/1: copiados da entrada, sem alterar.
- `<relacao>_evidencia_tratada`: os itens do Passo 3.5, um por linha, dentro da mesma célula.
  Vazio se a relação é 0 e a evidência está vazia.
- `<relacao>_evidencia_qnt`: número de itens `[OK]` + `[PARCIAL]` daquela relação.
  `[NAO_LOCALIZADO]` não conta. `0` se não houver itens.
- `<relacao>_categorias_rq01`: contagem por categoria principal, só dos itens que contam, no
  formato `test_instructions: 2; code_conventions: 1`.
- `itens_parciais`, `itens_nao_localizados`: totais da linha, somando as três relações.
- `observacoes`: inconsistências que valem revisão do anotador, por exemplo: relação marcada `1` cujos
  itens ficaram todos `[NAO_LOCALIZADO]`; relação marcada `0` com evidência preenchida (ou o
  contrário); sobreposição relevante que a evidência não menciona.

### 4.2 Saída longa (uma linha por item): `<PASTA_SAIDA>/rq02_evidence_items.csv`

```
repo, relacao, item_n, status, categoria_rq01, categoria_rq01_secundaria, descricao,
arquivo_a, linhas_a, trecho_a, arquivo_b, linhas_b, trecho_b
```

- `relacao`: `conflitantes`, `redundantes` ou `complementares`.
- `item_n`: 1, 2, 3... dentro de cada repositório × relação.
- `arquivo_b`, `linhas_b`, `trecho_b`: vazios quando só um arquivo contribui.

Grave as duas saídas em modo append (pandas com `mode="a", header=False`, ou equivalente). Nunca
reescreva o arquivo inteiro e nunca reprocesse um repositório que já está na saída 4.1.

## Passo 5 — Relate ao final do lote

Informe: quantos repositórios foram tratados nesta sessão, quantos faltam, os totais do lote
(itens OK, PARCIAL, NAO_LOCALIZADO) e as linhas com `observacoes`. Pare aqui, mesmo que caiba mais.


## Notas importantes

- Não altere os 0/1 da `ENTRADA`. Discordâncias vão em `observacoes`.
- Arquivos idênticos (mesmo conteúdo): um único item `redundante`, categoria = a categoria
  dominante do arquivo, e anote "arquivos idênticos" na descrição.
- Inconsistência dentro de um mesmo arquivo não é relação entre arquivos: não conta, vai para
  `observacoes`.
- Se a pasta do repositório ou um arquivo não existir, preencha `observacoes` com o problema e
  deixe as colunas de evidência vazias.
- Tudo roda localmente a partir de `data/collection/context_files/`. Não precisa de token.
