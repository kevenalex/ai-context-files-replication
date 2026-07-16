# Resultados de Ranqueamento

## Contexto
Esta pasta armazena os arquivos CSV gerados após o processamento dos dados brutos do SEART. O ranqueamento classifica os repositórios com base em uma pontuação composta de **Popularidade** e **Maturidade**.

## Esqueleto dos Dados (CSV)
Além das colunas originais do SEART, este arquivo adiciona:
- `popularity_score`: Média ponderada de estrelas, contribuidores e watchers.
- `maturity_score`: Média baseada na idade do projeto, commits e linhas de código.
- `rank_score`: Pontuação final combinada (com aplicação de penalidades para repositórios de tutoriais ou inflados).
- `rank`: Posição ordinal do repositório (1º, 2º, ...).

## Uso
Consumido pelo script `scripts/run_detect_context.py` para definir a amostra de repositórios que serão verificados.
