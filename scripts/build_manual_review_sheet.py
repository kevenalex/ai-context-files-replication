import os
import pandas as pd

FILES_MAPPING = {
    "AGENTS.md": "AGENTS.md",
    "CLAUDE.md": "CLAUDE.md",
    "COPILOT": ".github/copilot-instructions.md",
    "GEMINI.md": "GEMINI.md",
    "CURSOR": ".cursorrules"
}

def build_link(repo, file_label, branch="main"):
    """Monta o link direto do arquivo no GitHub (assume branch 'main')."""
    path = FILES_MAPPING.get(file_label, file_label)
    return f"https://github.com/{repo}/blob/{branch}/{path}"

def build_review_sheet(input_csv, output_csv):
    if not os.path.exists(input_csv):
        print(f"Erro: Arquivo de entrada {input_csv} não encontrado.")
        return

    df = pd.read_csv(input_csv)

    df_review = df[['repo', 'file1', 'file2']].copy()
    df_review['link_file1'] = df_review.apply(lambda r: build_link(r['repo'], r['file1']), axis=1)
    df_review['link_file2'] = df_review.apply(lambda r: build_link(r['repo'], r['file2']), axis=1)
    df_review['classificacao_manual'] = ""
    df_review['evidencia_manual'] = ""

    df_review = df_review[[
        'repo', 'file1', 'link_file1', 'file2', 'link_file2',
        'classificacao_manual', 'evidencia_manual'
    ]]

    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df_review.to_csv(output_csv, index=False)

    print(f"--- Sucesso! Planilha cega para análise manual salva em: {output_csv} ---")
    print(f"{len(df_review)} linhas ({df_review['repo'].nunique()} repositórios).")
    print("Aviso: os links assumem branch 'main'. Se der 404 ao abrir, troque '/main/' por '/master/' na URL.")

if __name__ == "__main__":
    INPUT = "data/oldData/rq02/sample.csv"
    OUTPUT = "data/oldData/rq02/manual_review_blind.csv"

    build_review_sheet(INPUT, OUTPUT)
