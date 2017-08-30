import logging
import os

import requests

BASE_ENDPOINT = 'https://api.zenhub.io/p1'
ISSUE_ENDPOINT = BASE_ENDPOINT + '/repositories/{repo_id}/issues/{issue_id}'

API_TOKEN = os.environ.get('ZENHUB_API_TOKEN')

logger = logging.getLogger(__file__)


# token is sent in the X-Authentication-Token header
def fetch_issue(repo_id=None, issue_id=None):
    """
    Fetch information about an issue from Zenhub
    """
    if not repo_id or not issue_id:
        raise ValueError

    issue_endpoint = ISSUE_ENDPOINT.format(repo_id=repo_id, issue_id=issue_id)
    headers = {'X-Authentication-Token': API_TOKEN}
    logger.warn('Zenhub fetch for issue: %s', issue_endpoint)
    return requests.get(issue_endpoint, headers=headers)
