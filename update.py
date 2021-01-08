import os
import requests
import time
#import json

start_time = time.time()

print("Getting token")
token = os.getenv("TOKEN")
owner = "BD103"

# ---- #
# Data #
# ---- #


class User:
    print("Getting user data")
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
    print("Getting starred repos")
    query = f"https://api.github.com/users/{owner}/starred"
    params = {}
    headers = {"Authorization": f"token {token}"}

    r = requests.get(query, headers=headers, params=params)

    data = r.json()
    num = len(data)


class Repo:
    print("Getting repo data")
    query = f"https://api.github.com/users/{owner}/repos"
    params = {}
    headers = {"Authorization": f"token {token}"}

    r = requests.get(query, headers=headers, params=params)

    data = r.json()

    commits = 0
    prs = 0
    issues = 0

    for i in data:
        print(i)
        full_name = i["full_name"]
        print("Getting data for repo: " + full_name)
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
    print("Getting some zen UwU")
    query = "https://api.github.com/zen"
    params = {}
    headers = {"Authorization": f"token {token}"}

    r = requests.get(query, headers=headers, params=params)

    data = r.text


# ---------- #
# Formatting #
# ---------- #

print("Reading template")
f = open("template.md", "rt")
template = f.read()
f.close()

print("Writing data")
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

end_time = time.time()
print("Process finished in " + str(round(end_time - start_time, 1)) + " seconds.")
