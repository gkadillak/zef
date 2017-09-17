import json

from collections import namedtuple

from ..facades import github_facade


def get_repositories(name, verbose=False, **search):
    results = github_facade.fetch_repositories(repo_name=name, verbose=verbose, **search)
    return json.loads(results.text)

def repository_id(name, verbose=False, **search):
    results = get_repositories(name=name, verbose=verbose, **search)
    # TODO: what if a user wants to count issues across repos?
    if not results or results.get('total_count') > 1:
        return

    repo = results.get('items') and results.get('items')[0]
    # TODO: create a namedtuple that can be accessed by attributes
    return repo.get('id')
