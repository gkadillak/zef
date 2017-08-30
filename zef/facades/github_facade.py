import logging
import os

import requests
from requests.auth import HTTPBasicAuth

from .. import exceptions

logger = logging.getLogger(__name__)

BASE_ENDPOINT = 'https://api.github.com'
REPO_ENDPOINT = BASE_ENDPOINT + 'repos/Getaround/getaround3'
MILESTONES = REPO_ENDPOINT + '/milestones'
SEARCH_ISSUES_ENDPOINT = BASE_ENDPOINT + '/search/issues'
MILESTONE_ISSUES = REPO_ENDPOINT + '/issues?milestone={milestone}'
SEARCH_REPOSITORIES_ENDPOINT = BASE_ENDPOINT + '/search/repositories'

ACCESS_TOKEN = os.environ.get('GITHUB_ACCESS_TOKEN')

PIPELINE_CHOICES_MAP = {
    'in_progress': 'In Progress',
    'new_issues': 'New Issues',
    'done': 'Done',
    'icebox': 'Icebox',
    'review': 'Review/QA',
    'backlog': 'Backlog'
}
## Helpers and wrappers
def authenticated(func):
    """Make sure that the user has credentials"""
    def inner(*args, **kwargs):
        if not ACCESS_TOKEN:
            raise exceptions.CredentialsNotFoundError
        return func(*args, **kwargs)
    return inner

def _assemble_search_query(base_search=None, **search):
    """
    Given keyword arguments, return the string to be used
    to query for the given entities for the search endpoint
    """
    query_str = '?q='
    query = query_str + base_search if base_search else query_str
    for key, value in search.items():
        query += '{key}:{value}+'.format(key=key, value=value) if value else '{key}+'.format(key=key)
    query = query.rstrip('+')
    return query

@authenticated
def fetch_milestones():
    """
    Retrieve the list of milestones for the given repository
    """
    auth = ('token', ACCESS_TOKEN)
    
    return requests.get(MILESTONES, auth=auth)

@authenticated
def fetch_issues_for_milestone(milestone_id):
    auth = ('token', ACCESS_TOKEN)
    endpoint = MILESTONE_ISSUES.format(milestone=milestone_id)

    return requests.get(endpoint, auth=auth)

@authenticated
def fetch_repositories(base_search, **search):
    """
    Fetch the information about a given repository

    @param str base_search: Title of the repository
    @param search: keyword arguments to be used to refine search
    """
    query = _assemble_search_query(base_search, **search)
    url = SEARCH_REPOSITORIES_ENDPOINT + query
    auth = ('gkadillak', ACCESS_TOKEN)
    logger.warn('Issues search: %s', query)
    return requests.get(url, auth=auth)

@authenticated
def fetch_search_issues(**search):
    """
    Search through all issues in github according to given
    options: https://developer.github.com/v3/search/#search-issues

    This endpoint doesn't have to be authenticated.

    @params: key, value pairs of search terms passed to github
    """
    if not all([search.keys()]):
        raise InsufficientSearchParametersError

    # TODO: add sort and created as extra query parameters. Not sure if needed now
    query = _assemble_search_query(**search)

    auth = ('gkadillak', ACCESS_TOKEN)
    url = SEARCH_ISSUES_ENDPOINT + query
    return requests.get(url, auth=auth)
