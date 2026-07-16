import os
import pandas as pd
import requests
import re
import time
import base64
import json
from dotenv import load_dotenv

load_dotenv()

FILES_MAPPING = {
    "AGENTS.md": "AGENTS.md",
    "CLAUDE.md": "CLAUDE.md",
    "COPILOT": ".github/copilot-instructions.md",
    "GEMINI.md": "GEMINI.md",
    "CURSOR": ".cursorrules"
}

TEST_KEYWORDS = [
    "test", "unit", "integration", "coverage", "verification", 
    "quality", "execute test", "testing", "typecheck", "lint"
]

def get_file_content_api(repo_name, file_path, token):
    url = f"https://api.github.com/repos/{repo_name}/contents/{file_path}"
    headers = {"Authorization": f"token {token}"} if token else {}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            content_b64 = response.json().get('content', '')
            content_bytes = base64.b64decode(content_b64)
            return content_bytes.decode('utf-8', errors='ignore')
    except:
        pass
    return None

def get_repo_tree(repo_name, token):
    """Obtém a lista recursiva de arquivos do repositório."""
    url_repo = f"https://api.github.com/repos/{repo_name}"
    headers = {"Authorization": f"token {token}"} if token else {}
    try:
        resp = requests.get(url_repo, headers=headers, timeout=10)
        if resp.status_code != 200: return []
        default_branch = resp.json().get('default_branch', 'main')
        
        url_tree = f"https://api.github.com/repos/{repo_name}/git/trees/{default_branch}?recursive=1"
        resp_tree = requests.get(url_tree, headers=headers, timeout=15)
        if resp_tree.status_code == 200:
            tree = resp_tree.json().get('tree', [])
            return [item['path'] for item in tree]
    except:
        pass
    return []

def extract_section_content(content, section_title, level):
    """Extrai o texto abaixo de um heading específico até o próximo heading de mesmo nível ou superior."""
    lines = content.split('\n')
    start_index = -1
    
    pattern = rf'^{"#" * level}\s+{re.escape(section_title)}'
    
    for i, line in enumerate(lines):
        if re.match(pattern, line, re.IGNORECASE):
            start_index = i + 1
            break
            
    if start_index == -1:
        return ""
    
    section_lines = []
    for line in lines[start_index:]:
        if re.match(r'^#{1,' + str(level) + r'}\s+', line):
            break
        section_lines.append(line)
        
    return '\n'.join(section_lines).strip()

def run_testing_extraction(classified_csv, output_json, github_token):
    if not os.path.exists(classified_csv):
        print(f"Erro: {classified_csv} não encontrado.")
        return

    df_structure = pd.read_csv(classified_csv)
    
    df_testing = df_structure[df_structure['category'].str.contains("Testing", na=False, case=False)].copy()
    
    if df_testing.empty:
        print("Nenhuma seção de teste encontrada para processar.")
        return

    grouped = df_testing.groupby(['repo', 'file_type'])
    
    results = []
    
    print(f"--- Processando {len(grouped)} arquivos com seções de teste ---")

    for (repo_name, file_type), group in grouped:
        print(f"Analisando {repo_name} ({file_type})...")
        
        file_path = FILES_MAPPING.get(file_type)
        content = get_file_content_api(repo_name, file_path, github_token)
        
        if not content:
            continue
            
        tree = get_repo_tree(repo_name, github_token)
        
        sections_data = []
        for _, row in group.iterrows():
            text = extract_section_content(content, row['title_original'], row['level'])
            sections_data.append({
                "heading": row['title_original'],
                "level": row['level'],
                "content": text
            })
            
        results.append({
            "repo": repo_name,
            "file_type": file_type,
            "testing_sections": sections_data,
            "file_tree": tree
        })
        
        time.sleep(0.1)

    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
        
    print(f"--- Sucesso! Detalhes salvos em: {output_json} ---")

if __name__ == "__main__":
    INPUT = "data/oldData/rq01/structure_analysis_classified.csv"
    OUTPUT = "data/oldData/misc/testing_analysis/testing_validity_data.json"
    TOKEN = os.getenv("GITHUB_TOKEN")
    
    run_testing_extraction(INPUT, OUTPUT, TOKEN)
