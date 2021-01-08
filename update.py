import os
import requests

token = os.getenv("TOKEN")
owner = "BD103"

# ---- #
# Data #
# ---- #


class User:
    query = f"https://api.github.com/users/{owner}"
    params = {}
    headers = {"Authorization": f"token {token}"}

    r = requests.get(
        query,
        headers=headers,
        params=params,
    )

    data = r.json()


class Starred:
    query = f"https://api.github.com/users/{owner}/starred"
    params = {}
    headers = {"Authorization": f"token {token}"}

    r = requests.get(query, headers=headers, params=params)

    data = r.json()
    num = len(data)


class Repo:
    query = f"https://api.github.com/users/{owner}/repos"
    params = {}
    headers = {"Authorization": f"token {token}"}

    r = requests.get(query, headers=headers, params=params)

    data = r.json()

    commits = 0
    prs = 0
    issues = 0

    for i in data:
        full_name = i["full_name"]
        query = f"https://api.github.com/repos/{full_name}/commits"
        params = {}
        headers = {"Authorization": f"token {token}"}

        r = requests.get(query, headers=headers, params=params)

        for i in r.json():
            if i["author"]["login"] == owner:
                commits += 1

        query = f"https://api.github.com/repos/{full_name}/pulls"
        params = {"state": "all"}
        headers = {"Authorization": f"token {token}"}

        r = requests.get(query, headers=headers, params=params)

        for i in r.json():
            if i["user"]["login"] == owner:
                prs += 1

        query = f"https://api.github.com/repos/{full_name}/issues"
        params = {"state": "all"}
        headers = {"Authorization": f"token {token}"}

        r = requests.get(query, headers=headers, params=params)

        for i in r.json():
            if i["user"]["login"] == owner:
                issues += 1

    # print(commits)
    # print(prs)
    # print(issues)


class Zen:
    query = "https://api.github.com/zen"
    params = {}
    headers = {"Authorization": f"token {token}"}

    r = requests.get(query, headers=headers, params=params)

    data = r.text


# ---------- #
# Formatting #
# ---------- #

f = open("template.md", "rt")
template = f.read()
f.close()

f = open("README.md", "wt")
f.write(
    template.format(
        stars=Starred.num,
        commits=Repo.commits,
        prs=Repo.prs,
        issues=Repo.issues,
        zen=Zen.data,
    )
)
f.close()
