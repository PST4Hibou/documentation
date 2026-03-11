repositories = []

with open("repos.list") as file:
    lines = [line.rstrip() for line in file]

    for repo in lines:
        if len(repo) != 0 and not repo.startswith("#"):
            elems = repo.split("@", 1)

            if len(elems) != 2:
                print(f"Invalid repo format (should be name@url): {repo}")
                continue

            out_dir, repo_url = elems[0], elems[1]

            if "/" in out_dir:
                print(f"Invalid repo format, no '/' allowed in the name: {repo}")
                continue

            repositories.append((out_dir, repo_url))
