#!/usr/bin/env python3

import os
from pathlib import Path
import subprocess
import sys

import repos


Path("./docs").mkdir(parents=True, exist_ok=True)

for out_dir, repo_url in repos.repositories:
    print("Generating docs for", out_dir)

    tmp_path = f"./tmp/{out_dir}"
    docs_path = f"./docs/{out_dir}/"

    # Check if running via uv, activate .venv if needed
    if not any("venv" in p for p in sys.path):
        result = subprocess.run(["uv", "python", "list"], capture_output=True, cwd=tmp_path)
        if result.returncode != 0:
            print("Failed to use the UV of", out_dir)
            print(result.stderr.decode("utf-8"))
            print(result.stdout.decode("utf-8"))
            exit(1)

    result = subprocess.run(["uv", "add", "griffe"], capture_output=True, cwd=tmp_path)
    if result.returncode != 0:
        print("Failed to add griffe to the UV of", out_dir)
        exit(1)

    # Run doc_build.py with uv run for this repo
    cmd = [
        "uv", "run", "--directory", ".", "--with", "griffe",
        "python", str(Path("./scripts/doc_build.py").resolve()),
        str(Path(tmp_path).resolve()), str(Path(docs_path).resolve())
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, cwd=tmp_path)
    if result.returncode != 0:
        print(f"Failed to generate docs for: {repo_url}")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        exit(1)

    print("STDOUT:", result.stdout)
