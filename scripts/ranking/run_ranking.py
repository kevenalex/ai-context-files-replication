import os
from unittest import mock

import pandas as pd
from scripts.ranking.ranking import rank_repositories

# ===========================
# SETTINGS
# ===========================

# SEART export of 2025-08-24 (see data/collection/README.md to obtain the full file)
INPUT_FILE = "data/collection/seart/seart_24-08-2025.json"

# The output goes to results/ so that it does not overwrite the ranking used in the study
# (data/collection/ranking/), which is the reference for the comparison at the end of the script.
OUTPUT_FOLDER = "results/collection/ranking_reproduction"
OUTPUT_RANKED = "ranked_24-08-2025.csv"
OUTPUT_TOP = "top10000_24-08-2025.csv"
TOP_N = 10000
STUDY_TOP = "data/collection/ranking/top10000_24-08-2025.csv"

# Ranking parameters (the same as in the replication package of Mohsenimofidi et al.)
WEIGHTS_POP = {"stargazers": 0.25, "contributors": 0.50, "watchers": 0.25}
WEIGHTS_MAT = {"projectAge": 1/3, "commits": 1/3, "codeLines": 1/3}
APPLY_PENALTIES = True

# ranking.py computes the project age from pd.Timestamp.now(). To reproduce the ranking used in
# the study, we fix the moment at which it was generated.
REFERENCE_DATE = pd.Timestamp("2026-04-01 05:51:42.5")

# The ranking used in the study has rank_score rounded to 2 decimals, which creates ties.
DECIMALS = 2

# Columns dropped from the top 10,000 to keep the file small (free text and lists)
DROPPED_COLUMNS_TOP = ["metrics", "languages", "labels", "topics", "homepage", "lastCommitSHA"]


def main():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    if not os.path.exists(INPUT_FILE):
        print(f"Error: file {INPUT_FILE} not found.")
        return

    print("--- Ranking ---")
    print(f"Input file: {INPUT_FILE}")

    with mock.patch("pandas.Timestamp.now", return_value=REFERENCE_DATE):
        df_ranked = rank_repositories(
            json_path=INPUT_FILE,
            popularity_weights=WEIGHTS_POP,
            maturity_weights=WEIGHTS_MAT,
            apply_penalties=APPLY_PENALTIES
        )

    df_ranked["rank_score"] = df_ranked["rank_score"].round(DECIMALS)
    df_ranked["rank"] = df_ranked["rank_score"].rank(ascending=False)
    df_ranked = df_ranked.sort_values("rank", kind="stable")

    df_ranked.to_csv(os.path.join(OUTPUT_FOLDER, OUTPUT_RANKED), index=False)
    top = df_ranked.head(TOP_N).drop(columns=DROPPED_COLUMNS_TOP, errors="ignore")
    top.to_csv(os.path.join(OUTPUT_FOLDER, OUTPUT_TOP), index=False)

    print(f"Ranked repositories: {len(df_ranked)}")
    print(f"Top {TOP_N} saved to: {os.path.join(OUTPUT_FOLDER, OUTPUT_TOP)}")
    print(df_ranked[["name", "rank_score"]].head(5).to_string(index=False))

    # Comparison with the top 10,000 used in the study
    study = pd.read_csv(STUDY_TOP, usecols=["name", "rank"])
    same_positions = (top["rank"].values == study["rank"].values).all()
    different = sorted(set(top["name"]) ^ set(study["name"]))
    print("\n--- Comparison with the study's top 10,000 ---")
    print(f"Identical positions (rank): {same_positions}")
    print(f"Different repositories: {len(different)} {different}")
    print("(expected: identical positions and 2 tied repositories at the cut-off; see data/collection/README.md)")


if __name__ == "__main__":
    main()
