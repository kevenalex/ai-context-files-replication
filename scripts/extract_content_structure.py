import os
import pandas as pd
import requests
import re
import time
import base64
from dotenv import load_dotenv

load_dotenv()

# Arquivos que você quer detectar e seus caminhos reais no repositório
FILES_MAPPING = {
    "AGENTS.md": "AGENTS.md",
    "CLAUDE.md": "CLAUDE.md",
    "COPILOT": ".github/copilot-instructions.md",
    "GEMINI.md": "GEMINI.md",
    "CURSOR": ".cursorrules"
}

def get_file_content_api(repo_name, file_path, token):
    """Obtém o conteúdo bruto de um arquivo via API do GitHub."""
    url = f"https://api.github.com/repos/{repo_name}/contents/{file_path}"
    headers = {"Authorization": f"token {token}"} if token else {}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            content_b64 = response.json().get('content', '')
            # A API retorna o conteúdo em base64 com quebras de linha
            content_bytes = base64.b64decode(content_b64)
            return content_bytes.decode('utf-8', errors='ignore')
    except Exception as e:
        # Silenciamos erros 404 comuns para não poluir o terminal
        pass
    return None

def extract_headings_with_levels(content):
    """Extrai cabeçalhos Markdown e seus níveis (# = 1, ## = 2, etc)."""
    if not content:
        return []
    
    # Regex para capturar níveis de # (ATX style)
    headings = re.findall(r'^(#{1,6})\s+(.+)$', content, re.MULTILINE)
    
    extracted = []
    for level_hashes, title in headings:
        extracted.append({
            "level": len(level_hashes),
            "title": title.strip()
        })
    return extracted

def normalize_title(title):
    """Aplica uma normalização básica no título para facilitar contagem."""
    normalized = re.sub(r'[^a-zA-Z\s]', '', title)
    normalized = normalized.lower().strip()
    return normalized

def run_structure_extraction(input_csv, output_csv, github_token, sample_size=None):
    """
    Percorre o CSV de detecção e extrai a estrutura de todos os arquivos encontrados.
    """
    if not os.path.exists(input_csv):
        print(f"Erro: Arquivo de entrada {input_csv} não encontrado.")
        return

    df = pd.read_csv(input_csv)
    if sample_size:
        df = df.head(sample_size)
    
    # Identificar colunas de arquivos presentes no mapeamento
    file_columns = [col for col in df.columns if col in FILES_MAPPING.keys()]
    
    all_data = []
    
    print(f"--- Iniciando Extração de Estrutura ({len(df)} repositórios) ---")
    print(f"Arquivos monitorados: {file_columns}")

    for index, row in df.iterrows():
        repo_name = row['name']
        
        for file_label in file_columns:
            if row[file_label] == 1:
                file_path = FILES_MAPPING[file_label]
                content = get_file_content_api(repo_name, file_path, github_token)
                
                if content:
                    headings = extract_headings_with_levels(content)
                    for h in headings:
                        all_data.append({
                            "repo": repo_name,
                            "file_type": file_label,
                            "level": h['level'],
                            "title_original": h['title'],
                            "title_normalized": normalize_title(h['title'])
                        })
                
                # Respeitar rate limit (ajustado para processamento em massa)
                time.sleep(0.05 if github_token else 1.0)
        
        if (index + 1) % 50 == 0:
            print(f"Progresso: {index + 1}/{len(df)} repositórios processados...")

    result_df = pd.DataFrame(all_data)
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    result_df.to_csv(output_csv, index=False)
    print(f"--- Sucesso! Dados salvos em: {output_csv} ---")

if __name__ == "__main__":
    # Configuração solicitada: Top 1000 de 23-03-2026
    INPUT = "data/oldData/rq01/ai_context_files_in_repositories/context_api_top1000_23-03-2026.csv"
    OUTPUT = "data/oldData/rq01/structure_analysis.csv"
    TOKEN = os.getenv("GITHUB_TOKEN")
    
    run_structure_extraction(INPUT, OUTPUT, TOKEN)
