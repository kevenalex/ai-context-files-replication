import os
import time
import base64
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

FILES_MAPPING = {
    "AGENTS.md": "AGENTS.md",
    "CLAUDE.md": "CLAUDE.md",
    "COPILOT": ".github/copilot-instructions.md",
    "GEMINI.md": "GEMINI.md",
    "CURSOR": ".cursorrules"
}

def get_file_content_api(repo_name, file_path, token):
    """Obtém o conteúdo bruto de um arquivo via API do GitHub (usa a branch default automaticamente)."""
    url = f"https://api.github.com/repos/{repo_name}/contents/{file_path}"
    headers = {"Authorization": f"token {token}"} if token else {}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            content_b64 = response.json().get('content', '')
            content_bytes = base64.b64decode(content_b64)
            return content_bytes.decode('utf-8', errors='ignore')
    except Exception:
        pass
    return None

def safe_repo_dirname(repo_name):
    """Converte 'owner/repo' em um nome de pasta seguro ('owner__repo')."""
    return repo_name.replace("/", "__")

def run_download(input_csv, output_dir, github_token):
    """Baixa todos os arquivos de contexto de IA presentes em cada repositório e
    grava um manifesto (CSV) com o caminho local de cada arquivo baixado."""
    if not os.path.exists(input_csv):
        print(f"Erro: Arquivo de entrada {input_csv} não encontrado.")
        return

    df = pd.read_csv(input_csv)
    file_columns = [col for col in df.columns if col in FILES_MAPPING]
    df['context_count'] = df[file_columns].sum(axis=1)
    df_target = df[df['context_count'] >= 1].reset_index(drop=True)

    os.makedirs(output_dir, exist_ok=True)
    manifest = []

    print(f"--- Iniciando download de arquivos de contexto de IA ({len(df_target)} repositórios) ---")

    for idx, row in df_target.iterrows():
        repo_name = row['name']
        repo_dir = os.path.join(output_dir, safe_repo_dirname(repo_name))

        for file_label in file_columns:
            if row[file_label] != 1:
                continue

            file_path = FILES_MAPPING[file_label]
            content = get_file_content_api(repo_name, file_path, github_token)

            if content:
                os.makedirs(repo_dir, exist_ok=True)
                local_filename = os.path.basename(file_path)
                local_path = os.path.join(repo_dir, local_filename)
                with open(local_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                manifest.append({"repo": repo_name, "file_label": file_label, "local_path": local_path, "status": "ok"})
            else:
                manifest.append({"repo": repo_name, "file_label": file_label, "local_path": "", "status": "falha"})

            time.sleep(0.05 if github_token else 1.0)

        if (idx + 1) % 50 == 0:
            print(f"Progresso: {idx + 1}/{len(df_target)} repositórios processados...")

    manifest_df = pd.DataFrame(manifest)
    manifest_path = os.path.join(output_dir, "download_manifest.csv")
    manifest_df.to_csv(manifest_path, index=False)

    qtd_ok = (manifest_df['status'] == 'ok').sum()
    qtd_falha = (manifest_df['status'] == 'falha').sum()
    print(f"--- Sucesso! {qtd_ok} arquivos baixados, {qtd_falha} falhas. Manifesto salvo em: {manifest_path} ---")

if __name__ == "__main__":
    INPUT = "data/oldData/rq01/ai_context_files_in_repositories/context_api_top10000_24-08-2025_20260507_070457.csv"
    OUTPUT_DIR = "data/oldData/rq01/rq00"
    TOKEN = os.getenv("GITHUB_TOKEN")

    run_download(INPUT, OUTPUT_DIR, TOKEN)
