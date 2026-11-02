"""Sample-based reproduction of the detection and download of the context files.

Redoing the detection on the 10,000 repositories takes about 50,000 GitHub API requests. This script
redoes both steps on a random sample of repositories from the top 10,000 and compares the result with
the study's data:

- detection: for each repository and format, whether the presence (0/1) matches that of 2026-05-07;
- download: for each file downloaded in the study, whether its current content is identical to that
  of 2026-06-24.

Differences are expected: repositories change over time (files are created, removed, or edited).
The result shows how much of the study's data still matches GitHub today.

Usage (from the repository root, with GITHUB_TOKEN in the .env file):
    python -m scripts.reproduce_collection_sample
"""
import os

import pandas as pd
from dotenv import load_dotenv

from scripts.detect_ai_context_files.detect_via_api import check_file_api
from scripts.download_ai_context_files import FILES_MAPPING, get_file_content_api

load_dotenv()

SAMPLE_SIZE = 50   # repositories drawn among the 1,256 with a file, and 50 among those without
SEED = 42
DETECTION = "data/collection/detection/detection_top10000_2026-05-07.csv"
FILES = "data/collection/context_files"
OUTPUT = "results/collection/sample_reproduction"


def main():
    token = os.getenv("GITHUB_TOKEN", "")
    os.makedirs(OUTPUT, exist_ok=True)
    det = pd.read_csv(DETECTION)
    formats = list(FILES_MAPPING)
    with_files = det[det[formats].sum(axis=1) > 0]
    without_files = det[det[formats].sum(axis=1) == 0]
    sample = pd.concat([with_files.sample(SAMPLE_SIZE, random_state=SEED),
                        without_files.sample(SAMPLE_SIZE, random_state=SEED)])
    print(f"Sample: {len(sample)} repositories ({SAMPLE_SIZE} with files and {SAMPLE_SIZE} without)")

    rows = []
    for _, row in sample.iterrows():
        repo = row["name"]
        for f in formats:
            now = int(check_file_api(repo, FILES_MAPPING[f], token))
            line = {"repo": repo, "format": f, "detected_in_study": int(row[f]), "detected_now": now,
                    "identical_content": ""}
            local = os.path.join(FILES, repo.replace("/", "__"), os.path.basename(FILES_MAPPING[f]))
            if row[f] == 1 and os.path.exists(local):
                current = get_file_content_api(repo, FILES_MAPPING[f], token)
                with open(local, encoding="utf-8") as fh:
                    line["identical_content"] = int(current is not None and current == fh.read())
            rows.append(line)

    res = pd.DataFrame(rows)
    res.to_csv(os.path.join(OUTPUT, "collection_sample.csv"), index=False)
    same = (res["detected_in_study"] == res["detected_now"])
    downloaded = res[res["identical_content"] != ""]
    print(f"Detection: {same.sum()} of {len(res)} decisions (repository × format) match the study "
          f"({100 * same.mean():.1f}%)")
    print(res[~same][["repo", "format", "detected_in_study", "detected_now"]].to_string(index=False))
    print(f"Download: {int(downloaded['identical_content'].astype(int).sum())} of {len(downloaded)} files "
          f"with content identical to that of 2026-06-24")
    print(f"Details in {OUTPUT}/collection_sample.csv")


if __name__ == "__main__":
    main()
