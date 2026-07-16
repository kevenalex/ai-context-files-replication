# Documentação de Coleta de Dados

**Ferramenta:** Extração realizada utilizando a ferramenta [seart](https://seart-ghs.si.usi.ch/)

**Data do download:** 16/06/2026

**Versão:** v1.17.1

## Filtros e Parâmetros Utilizados
| Parâmetro                  | Configuração Aplicada             | Objetivo Metodológico                                                  |
| :------------------------- | :-------------------------------- | :--------------------------------------------------------------------- |
| **Number of Contributors** | `≥ 2`                             | Eliminação de projetos individuais ou simples.                         |
| **Created Between**        | ` ≤ 01-01-2025`                   | Filtrar repositórios que tenham pelo menos um ano de existência        |
| **Last Commit**            | `Between 06-16-2025 - 06-16-2026` | Obter repositórios atualizados no máximo um ano atrás                  |
| **Forks**                  | `Exclude Forks`                   | Foco apenas nos projetos originais                                     |
| **Licence**                | `Has License`                     | Foco em projetos que possuem licenças, o que traz seriedade aos mesmos |

Assim como visto na imagem:

![Parâmetros SEART](seart_params.png)

### Notas Adicionais
Os dados brutos que foram utilizados nesta pesquisa podem ser acessados por este link https://zenodo.org/records/20724387

## Dados Brutos - SEART

### Contexto
Esta pasta deve conter os dados brutos exportados da ferramenta **SEART (Search GitHub Repositories)**. Estes arquivos JSON servem como o ponto de partida para todo o pipeline de pesquisa.

### Esqueleto dos Dados (JSON)
O arquivo é um objeto único com duas chaves: `parameters` (filtros aplicados na coleta, ver tabela acima) e `items` (lista de repositórios). Cada entrada de `items` representa um repositório e contém metadados como:
- `id`: Identificador interno (posição na coleta).
- `name`: Nome completo do repositório (`usuario/projeto`).
- `mainLanguage`: Linguagem principal detectada.
- `stargazers`, `forks`, `watchers`: Métricas de popularidade.
- `commits`, `contributors`, `releases`, `branches`: Métricas de atividade.
- `createdAt`, `pushedAt`, `updatedAt`, `lastCommit`, `lastCommitSHA`: Datas e hash do último commit.
- `size`, `blankLines`, `codeLines`, `commentLines`: Métricas de tamanho do código.
- `metrics`: Lista com a quebra de linhas (branco/código/comentário) por linguagem.
- `languages`: Dicionário `linguagem -> bytes` de código.
- `license`, `homepage`, `topics`, `labels`: Metadados adicionais do GitHub.
- `isFork`, `isArchived`, `isDisabled`, `isLocked`, `hasWiki`: Flags booleanas de estado do repositório.

### Exemplo de Registro
Abaixo, um exemplo real (`sparklemotion/nokogiri`) com listas longas truncadas para legibilidade:

```json
{
  "id": 0,
  "name": "sparklemotion/nokogiri",
  "isFork": false,
  "commits": 7987,
  "branches": 51,
  "releases": 89,
  "forks": 934,
  "mainLanguage": "C",
  "defaultBranch": "main",
  "license": "MIT License",
  "homepage": "https://nokogiri.org/",
  "watchers": 148,
  "stargazers": 6255,
  "contributors": 241,
  "size": 45652,
  "createdAt": "2008-07-14T03:34:32",
  "pushedAt": "2026-05-07T09:12:55",
  "updatedAt": "2026-05-09T01:22:41",
  "totalIssues": 2056,
  "openIssues": 73,
  "totalPullRequests": 1427,
  "openPullRequests": 31,
  "blankLines": 14729,
  "codeLines": 128857,
  "commentLines": 15999,
  "metrics": [
    { "blankLines": 0, "codeLines": 84, "commentLines": 0, "language": "XHTML" },
    { "blankLines": 9, "codeLines": 58, "commentLines": 0, "language": "XSLT" }
    // ... (+24 itens, um por linguagem)
  ],
  "lastCommit": "2026-05-07T09:11:54",
  "lastCommitSHA": "7ab68ffca6863ff130b35a00625f987641ee02db",
  "hasWiki": true,
  "isArchived": false,
  "isDisabled": false,
  "isLocked": false,
  "languages": { "C": 1483780, "Ruby": 1316244, "Java": 662918 /* ... */ },
  "labels": ["backport", "blocked", "dependencies" /* ... (+63 labels) */],
  "topics": ["libxml2", "libxslt", "nokogiri", "ruby", "ruby-gem", "sax", "xerces", "xml", "xslt"]
}
```

Mais 4 exemplos completos (sem truncamento) estão disponíveis em [`06-16-2026-seart_data_sample.json`](./06-16-2026-seart_data_sample.json), extraídos do arquivo bruto via amostragem em streaming (sem carregar o JSON completo em memória).

### Uso
Estes arquivos são consumidos pelo script `scripts/ranking/run_ranking.py` para gerar a lista ranqueada de repositórios.



