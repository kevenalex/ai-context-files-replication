import os
from datetime import datetime
from dotenv import load_dotenv
from scripts.detect_ai_context_files.detect_via_api import detect_context_api
from scripts.detect_ai_context_files.detect_via_clone import detect_context_clone

load_dotenv()

# ==============================================================================
# CONFIGURAÇÃO DA DETECÇÃO
# ==============================================================================

# MODO DE ANÁLISE: "API" ou "CLONE"
MODE = "API"

# Parâmetros de entrada e amostragem
INPUT_CSV = "data/oldData/rq01/output_rankings/ranked_24-08-2025.csv"
OUTPUT_FOLDER = "data/oldData/rq01/ai_context_files_in_repositories"
SAMPLE_SIZE = 10000

# Paralelismo: Apenas para o modo "CLONE"
WORKERS = 5

# Token do GitHub: O script tenta pegar do .env
TOKEN = os.getenv("GITHUB_TOKEN", "")

# Arquivos que você quer detectar
FILES_TO_FIND = {
    "AGENTS.md": "AGENTS.md",
    "CLAUDE.md": "CLAUDE.md",
    "COPILOT": ".github/copilot-instructions.md",
    "GEMINI.md": "GEMINI.md",
    "CURSOR": ".cursorrules"
}

# ==============================================================================

def main():
    if not os.path.exists(INPUT_CSV):
        print(f"Erro: Arquivo {INPUT_CSV} não encontrado.")
        return

    if MODE == "API":
        df_results = detect_context_api(
            input_csv=INPUT_CSV,
            output_folder=OUTPUT_FOLDER,
            sample_size=SAMPLE_SIZE,
            github_token=TOKEN,
            context_files=FILES_TO_FIND
        )
    elif MODE == "CLONE":
        df_results = detect_context_clone(
            input_csv=INPUT_CSV,
            output_folder=OUTPUT_FOLDER,
            sample_size=SAMPLE_SIZE,
            context_files=FILES_TO_FIND,
            max_workers=WORKERS
        )
    else:
        print(f"Erro: Modo de análise '{MODE}' desconhecido. Escolha 'API' ou 'CLONE'.")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = os.path.basename(INPUT_CSV).replace("ranked_", f"context_{MODE.lower()}_top{SAMPLE_SIZE}_").replace(".csv", "")
    output_path = os.path.join(OUTPUT_FOLDER, f"{base_name}_{timestamp}.csv")

    df_results.to_csv(output_path, index=False)
    
    print(f"\nSucesso! Ranking salvo em: {output_path}")
    
    print("\nRESUMO DE ADOÇÃO:")
    for label in FILES_TO_FIND.keys():
        total = df_results[label].sum()
        print(f"- {label}: {total} repositórios")

if __name__ == "__main__":
    main()
