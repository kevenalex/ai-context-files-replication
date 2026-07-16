import os
import math
import pandas as pd

def calculate_sample_size(population_size, confidence_z, margin_error, p=0.5):
    """Fórmula de Cochran com correção para população finita."""
    n0 = (confidence_z ** 2 * p * (1 - p)) / (margin_error ** 2)
    n = n0 / (1 + (n0 - 1) / population_size)
    return math.ceil(n)

def run_sample_selection(input_csv, output_csv, confidence_z, margin_error, random_state):
    if not os.path.exists(input_csv):
        print(f"Erro: Arquivo de entrada {input_csv} não encontrado.")
        return

    df = pd.read_csv(input_csv)
    unique_repos = df['repo'].drop_duplicates().reset_index(drop=True)
    population_size = len(unique_repos)

    sample_size = calculate_sample_size(population_size, confidence_z, margin_error)
    sampled_repos = unique_repos.sample(n=sample_size, random_state=random_state)

    df_sample = df[df['repo'].isin(sampled_repos)].copy()

    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df_sample.to_csv(output_csv, index=False)

    print("--- Cálculo da amostra (fórmula de Cochran com correção finita) ---")
    print(f"População (repositórios únicos): {population_size}")
    print(f"Confiança (Z): {confidence_z} | Margem de erro: {margin_error * 100:.0f}%")
    print(f"Tamanho da amostra (N): {sample_size}")
    print(f"--- Sucesso! {len(df_sample)} linhas ({sample_size} repositórios) salvas em: {output_csv} ---")

if __name__ == "__main__":
    INPUT = "data/oldData/rq02/semantic_analysis_rq01.csv"
    OUTPUT = "data/oldData/rq02/sample.csv"
    CONFIDENCE_Z = 1.645  # 90% de confiança
    MARGIN_ERROR = 0.10   # 10%
    RANDOM_STATE = 42

    run_sample_selection(INPUT, OUTPUT, CONFIDENCE_Z, MARGIN_ERROR, RANDOM_STATE)
