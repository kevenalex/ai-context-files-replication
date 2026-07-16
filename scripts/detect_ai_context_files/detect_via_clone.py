import os
import pandas as pd
import subprocess
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed

def check_files_clone(repo_name, context_files, temp_dir="temp_repos"):
    """Verifica arquivos clonando o repositório (shallow clone)."""
    repo_url = f"https://github.com/{repo_name}.git"
    folder_name = repo_name.replace("/", "___")
    target_path = os.path.join(temp_dir, folder_name)
    
    found = {label: 0 for label in context_files.keys()}
    
    try:
        subprocess.run(
            ["git", "clone", "--depth", "1", "--single-branch", repo_url, target_path],
            check=True, capture_output=True, text=True
        )
        
        for label, path in context_files.items():
            if os.path.exists(os.path.join(target_path, path)):
                found[label] = 1
                
    except Exception:
        pass
    finally:
        if os.path.exists(target_path):
            shutil.rmtree(target_path, ignore_errors=True)
            
    return repo_name, found

def detect_context_clone(
    input_csv,
    output_folder,
    sample_size=1000,
    context_files=None,
    max_workers=10,
    temp_dir="temp_repos"
):
    """Analisa repositórios via clonagem Git em paralelo."""
    if context_files is None:
        context_files = {"AGENTS.md": "AGENTS.md", "CLAUDE.md": "CLAUDE.md"}

    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(temp_dir, exist_ok=True)

    df = pd.read_csv(input_csv).head(sample_size)
    repos = df['name'].tolist()
    rank_map = dict(zip(df['name'], df['rank']))
    
    results = []
    
    print(f"--- Iniciando Detecção via Clonagem (Threads: {max_workers}) ---")
    print(f"Analisando os top {len(df)} repositórios...")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(check_files_clone, repo, context_files, temp_dir) for repo in repos]
        
        completed = 0
        for future in as_completed(futures):
            repo_name, found_local = future.result()
            
            data = {"name": repo_name, "rank": rank_map[repo_name]}
            data.update(found_local)
            results.append(data)
            
            completed += 1
            if completed % 10 == 0:
                print(f"Progresso: {completed}/{len(repos)}...")

    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir, ignore_errors=True)

    return pd.DataFrame(results)
