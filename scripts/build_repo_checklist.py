import os
import pandas as pd

def build_repo_checklist(input_csv, output_csv):
    if not os.path.exists(input_csv):
        print(f"Erro: Arquivo de entrada {input_csv} não encontrado.")
        return

    df = pd.read_csv(input_csv)

    files_by_repo = {}
    for _, row in df.iterrows():
        repo = row['repo']
        files_by_repo.setdefault(repo, {})
        files_by_repo[repo][row['file1']] = row['link_file1']
        files_by_repo[repo][row['file2']] = row['link_file2']

    rows = []
    for repo, files_dict in files_by_repo.items():
        file_names = sorted(files_dict.keys())
        rows.append({
            'repo': repo,
            'qtd_arquivos': len(file_names),
            'arquivos_para_analisar': '; '.join(file_names),
            'links_arquivos': '; '.join(files_dict[f] for f in file_names),
            'status': 'Pendente'
        })

    df_checklist = pd.DataFrame(rows).sort_values('repo').reset_index(drop=True)

    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df_checklist.to_csv(output_csv, index=False)

    print(f"--- Sucesso! Checklist por repositório salvo em: {output_csv} ---")
    print(f"{len(df_checklist)} repositórios.")

if __name__ == "__main__":
    INPUT = "data/oldData/rq02/sample_to_manual_review_24-06-2026.csv"
    OUTPUT = "data/oldData/rq02/repo_checklist.csv"

    build_repo_checklist(INPUT, OUTPUT)
