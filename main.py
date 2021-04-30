from github import Github
import os
from func import get_stats

g = Github(os.environ["token"])


print(get_stats(g))