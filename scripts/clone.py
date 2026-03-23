#!/usr/bin/env python3

import os
import repos
from pathlib import Path


Path("./tmp").mkdir(parents=True, exist_ok=True)

for out_dir, repo_url in repos.repositories:
    print("Cloning repo:", repo_url, "into", out_dir)
    if os.system(f"git clone {repo_url} ./tmp/{out_dir}") != 0:
        print(f"Failed to clone repo: {repo_url}")
        exit(1)
