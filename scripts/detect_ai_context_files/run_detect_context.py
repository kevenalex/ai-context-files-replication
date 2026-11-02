import os
from datetime import datetime
from dotenv import load_dotenv
from scripts.detect_ai_context_files.detect_via_api import detect_context_api

load_dotenv()

# ==============================================================================
# DETECTION SETTINGS
# ==============================================================================

INPUT_CSV = "data/collection/ranking/top10000_24-08-2025.csv"
# A new detection goes to results/ so that it does not overwrite the one used in the study.
OUTPUT_FOLDER = "results/collection/detection_rerun"
SAMPLE_SIZE = 10000

# GitHub token, read from the .env file
TOKEN = os.getenv("GITHUB_TOKEN", "")

# Default path of each format in the repository
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
        print(f"Error: file {INPUT_CSV} not found.")
        return

    df_results = detect_context_api(
        input_csv=INPUT_CSV,
        output_folder=OUTPUT_FOLDER,
        sample_size=SAMPLE_SIZE,
        github_token=TOKEN,
        context_files=FILES_TO_FIND
    )

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    date = datetime.now().strftime("%Y-%m-%d")
    output_path = os.path.join(OUTPUT_FOLDER, f"detection_top{SAMPLE_SIZE}_{date}.csv")

    df_results.to_csv(output_path, index=False)

    print(f"\nDone! Detection saved to: {output_path}")

    print("\nADOPTION SUMMARY:")
    for label in FILES_TO_FIND.keys():
        total = df_results[label].sum()
        print(f"- {label}: {total} repositories")

if __name__ == "__main__":
    main()
