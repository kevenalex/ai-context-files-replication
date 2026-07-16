import os
import pandas as pd
import requests
import time

def check_file_api(repo_name, file_path, token):
    """Verifica se um arquivo existe via API do GitHub."""
    url = f"https://api.github.com/repos/{repo_name}/contents/{file_path}"
    headers = {"Authorization": f"token {token}"} if token else {}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        return response.status_code == 200
    except:
        return False

def detect_context_api(
    input_csv,
    output_folder,
    sample_size=None,
    github_token="",
    context_files=None
):
    """Analisa repositórios via API do GitHub."""
    if context_files is None:
        print("Erro: context_files não fornecido.")
        return
    if sample_size is None:
        print("Erro: sample_size não fornecido.")
        return

    os.makedirs(output_folder, exist_ok=True)
    df = pd.read_csv(input_csv).head(sample_size)
    results = []
    
    print(f"--- Iniciando Detecção via API (Top {len(df)}) ---")

    for index, row in df.iterrows():
        repo_name = row['name']
        found_data = {"name": repo_name, "rank": row['rank']}
        
        for label, path in context_files.items():
            exists = check_file_api(repo_name, path, github_token)
            found_data[label] = 1 if exists else 0
        
        results.append(found_data)
        # time.sleep(0.1 if github_token else 1.0)
        
        if (index + 1) % 10 == 0:
            print(f"Processados: {index + 1}/{len(df)}...")

    return pd.DataFrame(results)
