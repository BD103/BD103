from github.MainClass import Github


def get_stats(g:Github):
  return {
    "repo_count": len([ i for i in g.get_user().get_repos()]),
    "starred_repos": len([ i for i in g.get_user().get_starred()]),
    #"commits": len([ i for i in g.get_user().get_repos()])
  }