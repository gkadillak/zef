import click
import logging
import os
import requests

from requests.auth import HTTPBasicAuth

from zef import exceptions
from zef import settings


BASE_ENDPOINT = 'https://api.github.com'
REPO_ENDPOINT = BASE_ENDPOINT + '/repos/Getaround/getaround3'
SEARCH_ISSUES_ENDPOINT = BASE_ENDPOINT + '/search/issues'
SEARCH_REPOSITORIES_ENDPOINT = BASE_ENDPOINT + '/search/repositories'

## Helpers and wrappers
# TODO: create a single helper that makes requests so you
# only have to check once if request is authenticated
def authenticated(func):
    """
    Decorator to ensure that credentials for the request are availabl

    @raises exceptions.CredentialsNotFoundError
    """
    def inner(*args, **kwargs):
        if not settings.GITHUB_ACCESS_TOKEN:
            raise exceptions.CredentialsNotFoundError('Environmental variable not found: GITHUB_ACCESS_TOKEN')
        return func(*args, **kwargs)
    return inner

def _assemble_search_query(base_search=None, verbose=False, **search):
    """
    Takes keyword arguments and converts them into a query string
    that can be used for the search endpoint in Github

    >>> _assemble_search_query(base_search='windows', label='bug', language='python')
    '?q=windows+label:bug+language:python'

    >>> _assemble_search_query(base_search=None, label='feature', assignee='gkadillak')
    '?q=label:feature+assignee:gkadillak'

    @param base_search str: The endoint
    @param verbose bool: Print the request to stdout
    @param search dict: Values to use to create query

    @rtype: str
    @return: Endpoint with query string for Github
    """
    query_str = '?q='
    query = query_str + base_search if base_search else query_str
    search_format = '+{key}:{value}' if base_search else '{key}:{value}+'

    for key, value in search.items():
        query += search_format.format(key=key, value=value) if value else '{key}+'.format(key=key)
    query = query.rstrip('+')
    if verbose:
        click.echo('Request to Github: %s' % query)
    return query

@authenticated
def fetch_repositories(repo_name, verbose=False, **search):
    """
    Fetch the information about a given repository

    @param str base_search: Title of the repository
    @param search: Keyword arguments to be used to refine search

    @return: Response from GET request
    """
    query = _assemble_search_query(base_search=repo_name, verbose=verbose, **search)
    url = SEARCH_REPOSITORIES_ENDPOINT + query
    auth = (settings.GITHUB_USERNAME, settings.GITHUB_ACCESS_TOKEN)
    return requests.get(url, auth=auth)

@authenticated
def fetch_search_issues(verbose=False, **search):
    """
    Search through all issues in github according to given
    options: https://developer.github.com/v3/search/#search-issues

    This endpoint doesn't have to be authenticated.

    @params: key, value pairs of search terms passed to Github

    @return: Response from GET request
    """
    if not all([search.keys()]):
        raise InsufficientSearchParametersError

    # TODO: add sort and created as extra query parameters. Not sure if needed now
    query = _assemble_search_query(verbose=verbose, **search)

    auth = (settings.GITHUB_USERNAME, settings.GITHUB_ACCESS_TOKEN)
    url = SEARCH_ISSUES_ENDPOINT + query
    return requests.get(url, auth=auth)
