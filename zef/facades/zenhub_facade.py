import click
import logging
import os

import requests

BASE_ENDPOINT = 'https://api.zenhub.io/p1'

ISSUE_ENDPOINT = BASE_ENDPOINT + '/repositories/{repo_id}/issues/{issue_id}'
BOARD_ENDPOINT = BASE_ENDPOINT + '/repositories/{repo_id}/board'

API_TOKEN = os.environ.get('ZENHUB_API_TOKEN')


def _get_request(endpoint, verbose):
    """
    Make a GET request to the given endpoint

    @param str endpoint: Query for resource

    @return Response
    @rtype: requests.models.Response
    """
    headers = {'X-Authentication-Token': API_TOKEN}
    if verbose:
        click.echo('Zenhub request: %s' % endpoint)
    return requests.get(endpoint, headers=headers)

# token is sent in the X-Authentication-Token header
def fetch_issue(repo_id=None, issue_id=None, verbose=False):
    """
    Fetch information about an issue from Zenhub
    """
    if not repo_id or not issue_id:
        raise ValueError('Repo ID and issue ID necessary for request')

    issue_endpoint = ISSUE_ENDPOINT.format(repo_id=repo_id, issue_id=issue_id)
    return _get_request(issue_endpoint, verbose=verbose)

def fetch_board(repo_id, verbose=False):
    """
    Fetch the details of the board for a given sprint. This returns all
    issues for all pipelines for the board excluding the closed issues.
    For these issues, the github API is needed.

    @param int repo_id: Number identifier of the repository (from github)

    @return Board information
    @rtype requests.models.Response
    """
    if not repo_id:
        raise ValueError('Repo ID needed to make request')

    board_endpoint = BOARD_ENDPOINT.format(repo_id=repo_id)
    return _get_request(board_endpoint, verbose=verbose)
