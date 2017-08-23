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
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')

PIPELINE_CHOICES_MAP = {
    'in_progress': 'In Progress',
    'new_issues': 'New Issues',
    'done': 'Done',
    'icebox': 'Icebox',
    'review': 'Review/QA',
    'backlog': 'Backlog'
}

def authenticated(func):
    """Make sure that the user has credentials"""
    def inner(*args, **kwargs):
        if not ACCESS_TOKEN:
            raise exceptions.CredentialsNotFoundError
        return func(*args, **kwargs)
    return inner

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
    query = '?q='
    for key, value in search.items():
        query += '{key}:{value}+'.format(key=key, value=value) if value else '{key}+'.format(key=key)
    query = query.rstrip('+')

    auth = ('token', ACCESS_TOKEN)
    url = SEARCH_ISSUES_ENDPOINT + query
    logger.info('Issues search: %s' % query)
    return requests.get(url, auth=auth)
