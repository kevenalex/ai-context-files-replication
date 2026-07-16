# Análise de Fidelidade de Testes

## Contexto
Armazena dados detalhados que cruzam as instruções de teste encontradas nos arquivos de contexto com a realidade física (árvore de arquivos) do repositório.

## Esqueleto dos Dados (JSON)
O arquivo `testing_validity_data.json` contém:
- `repo`: Nome do repositório.
- `file_type`: Tipo do arquivo de origem (ex: `AGENTS.md`).
- `testing_sections`: Lista de objetos com `heading` e `content` especificamente sobre testes.
- `file_tree`: Lista completa (ou amostra) de arquivos existentes no repositório para validação de caminhos e frameworks.

## Uso
Consumido pelo notebook `notebooks/6.1-test-validity-checker.ipynb` para calcular o *Alignment Score* (Índice de Alinhamento).
