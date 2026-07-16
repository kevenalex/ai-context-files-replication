import os
import re
import pandas as pd

# Mesma taxonomia de scripts/classify_headings.py (ordem importa: específicas antes das gerais)
TAXONOMY = {
    "Testing Strategy / Guidelines": ["testing strategy", "testing guideline", "testing principles"],
    "Testing Instructions": ["test", "unit", "integration", "coverage", "verification", "quality", "execute test", "testing cheatsheet", "test type", "typecheck", "lint", "type checking"],
    "Architecture / Project Structure": ["architecture", "structure", "layout", "folder", "directory", "module", "component", "organization", "tech stack", "technology stack", "key component", "important file", "backend", "frontend", "configuration flag", "feature flag", "database", "migration", "generated file", "key directories", "key files", "files and directories"],
    "Code Conventions / Best Practices": ["convention", "best practice", "style", "lint", "format", "naming", "rule", "guideline", "coding style", "javadoc", "comment", "header", "formatting", "import", "error handling", "logging", "dependency hygiene", "suppression", "documentation", "syntax note", "compatibility", "after writing", "after code", "code standards", "coding standards", "pitfall"],
    "Contribution Guidelines": ["contribution", "git", "pr", "pull request", "commit", "branch", "issue", "contributor", "developer workflow", "repository guideline", "changelog", "making changes"],
    "Getting Started / Setup": ["setup", "install", "environment", "prerequisite", "requirement", "dependency", "toolchain", "getting started", "initial setup", "quick start", "dependencies"],
    "Run / Build Commands": ["command", "build", "run", "workflow", "script", "compile", "execution", "usage", "deploy", "automation", "task", "essential command", "server", "refresh", "reset", "tool", "development", "code generation"],
    "Project Description": ["overview", "intro", "purpose", "goal", "description", "concept", "about", "vision", "functional", "capability", "instruction", "guide", "skill", "agentsmd", "claudemd"],
    "Troubleshooting": ["troubleshoot", "debug", "fix", "problem", "diagnosis"],
    "Security": ["security", "secret", "auth", "access", "privacy"],
    "Doc Metadata / Front-matter": ["metadata", "front-matter", "sidebar", "tag"],
    "Reference & Examples": ["reference", "cheat-sheet", "tip", "pattern", "example", "sample", "use case", "template", "finding related code", "note", "working with", "context-aware", "resource", "additional resources", "performance", "general", "configuration"]
}
CATEGORIES = list(TAXONOMY.keys()) + ["Other"]

def extract_headings_with_levels(content):
    """Extrai cabeçalhos Markdown (estilo ATX) via Regex."""
    if not content:
        return []
    headings = re.findall(r'^(#{1,6})\s+(.+)$', content, re.MULTILINE)
    return [{"level": len(h), "title": t.strip()} for h, t in headings]

def normalize_title(title):
    normalized = re.sub(r'[^a-zA-Z\s]', '', title)
    return normalized.lower().strip()

def classify_heading(title_normalized):
    if not isinstance(title_normalized, str):
        return "Other"
    for category, keywords in TAXONOMY.items():
        for kw in keywords:
            if kw in title_normalized:
                return category
    return "Other"

def repo_to_url(repo_name):
    return f"https://github.com/{repo_name}"

def run_repo_level_classification(manifest_csv, output_csv):
    """Classifica o conteúdo dos arquivos de contexto de IA já baixados (scripts/download_ai_context_files.py),
    agregando por repositório: uma coluna booleana por categoria + lista final das categorias encontradas."""
    if not os.path.exists(manifest_csv):
        print(f"Erro: Manifesto {manifest_csv} não encontrado.")
        return

    manifest = pd.read_csv(manifest_csv)
    manifest_ok = manifest[manifest['status'] == 'ok']

    print(f"--- Classificando conteúdo de {manifest_ok['repo'].nunique()} repositórios (arquivos já baixados em disco) ---")

    results = []
    for repo_name, group in manifest_ok.groupby('repo'):
        categories_present = {cat: False for cat in CATEGORIES}

        for _, file_row in group.iterrows():
            with open(file_row['local_path'], 'r', encoding='utf-8') as f:
                content = f.read()

            for heading in extract_headings_with_levels(content):
                category = classify_heading(normalize_title(heading['title']))
                categories_present[category] = True

        result_row = {"repo": repo_to_url(repo_name)}
        result_row.update(categories_present)
        result_row["categorias_encontradas"] = "; ".join(cat for cat, present in categories_present.items() if present)
        results.append(result_row)

    result_df = pd.DataFrame(results)
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    result_df.to_csv(output_csv, index=False)
    print(f"--- Sucesso! {len(result_df)} repositórios salvos em: {output_csv} ---")

if __name__ == "__main__":
    MANIFEST = "data/oldData/rq01/rq00/download_manifest.csv"
    OUTPUT = "data/oldData/rq01/regex_analysis_content_ai_context_files.csv"

    run_repo_level_classification(MANIFEST, OUTPUT)
