import os
import pandas as pd
from scripts.ranking.ranking import rank_repositories

# ===========================
# CONFIGURAÇÃO DA PESQUISA
# ===========================

# Caminho dos dados (Pasta input-data dentro do repositório)
INPUT_FILE = "data/newData/input_data/06-16-2026-seart_data_raw.json"

# Pasta de destino para os resultados
OUTPUT_FOLDER = "data/newData/rq01/output_rankings"

# Parâmetros do Ranking
WEIGHTS_POP = {"stargazers": 0.25, "contributors": 0.50, "watchers": 0.25}
WEIGHTS_MAT = {"projectAge": 1/3, "commits": 1/3, "codeLines": 1/3}
APPLY_PENALTIES = True

def main():
    # Garante que a pasta de output exista
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Verifica se o arquivo de entrada existe
    if not os.path.exists(INPUT_FILE):
        print(f"Erro: Arquivo {INPUT_FILE} não encontrado.")
        return

    # Gera o nome do arquivo de saída
    file_name = os.path.basename(INPUT_FILE).replace(".json", ".csv").replace(".gz", ".csv")
    output_path = os.path.join(OUTPUT_FOLDER, f"ranked_{file_name}")

    print(f"--- Iniciando Ranking ---")
    print(f"Processando arquivo: {INPUT_FILE}")

    try:
        # Executa o algoritmo de ranking
        df_ranked = rank_repositories(
            json_path=INPUT_FILE,
            popularity_weights=WEIGHTS_POP,
            maturity_weights=WEIGHTS_MAT,
            apply_penalties=APPLY_PENALTIES
        )

        # Salva o resultado final em CSV
        df_ranked.to_csv(output_path, index=False)
        
        # Quantidade total de repositórios analisados
        total_repos = len(df_ranked)
        
        print(f"Sucesso! Ranking salvo em: {output_path}")
        print(f"Total de repositórios analisados: {total_repos}")
        
        print("\n-------- TOP 5 ENCONTRADOS --------")
        print(df_ranked[['name', 'rank_score']].head(5).to_string(index=False))
        print("-----------------------------------\n")

    except Exception as e:
        print(f"Erro durante a execução: {e}")

if __name__ == "__main__":
    main()
