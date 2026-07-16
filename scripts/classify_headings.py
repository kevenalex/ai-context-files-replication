import pandas as pd
import re
import os

# Caminhos de arquivos
INPUT_FILE = "data/oldData/rq01/structure_analysis.csv"
OUTPUT_FILE = "data/oldData/rq01/structure_analysis_classified.csv"

# Taxonomia expandida baseada no material de referência "Context Engineering for AI Agents"
# A ordem importa: categorias mais específicas devem vir antes das gerais.
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

def classify_heading(title):
    if not isinstance(title, str):
        return "Other"
    
    title = title.lower()
    for category, keywords in TAXONOMY.items():
        for kw in keywords:
            if kw in title:
                return category
    return "Other"

def run_classification():
    if not os.path.exists(INPUT_FILE):
        print(f"Erro: Arquivo {INPUT_FILE} não encontrado.")
        return

    print(f"--- Lendo dados de {INPUT_FILE} ---")
    df = pd.read_csv(INPUT_FILE)
    
    print("--- Aplicando classificação semântica ---")
    df['category'] = df['title_normalized'].apply(classify_heading)
    
    # Salvar resultados
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"--- Sucesso! Dados classificados salvos em: {OUTPUT_FILE} ---")
    
    # Exibir estatísticas rápidas
    print("\nDistribuição de Categorias:")
    print(df['category'].value_counts())

if __name__ == "__main__":
    run_classification()
