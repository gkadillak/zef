import json

from collections import namedtuple

from ..facades import github_facade


def get_repositories(name, **search):
    results = github_facade.fetch_repositories(name, **search)
    return json.loads(results.text)

def repository_id(name, **search):
    results = get_repositories(name, **search)
    if not results or results.get('total_count') > 1:
        return

    repo = results.get('items')[0]
    # TODO: create a namedtuple that can be accessed by attributes
    return repo.get('id')
