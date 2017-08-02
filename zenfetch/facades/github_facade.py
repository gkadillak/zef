import os

import requests
from requests.auth import HTTPBasicAuth

from ..exceptions import CredentialsNotFoundError

ENDPOINT = 'https://api.github.com/repos/Getaround/getaround3'
MILESTONES = ENDPOINT + '/milestones'
MILESTONE_ISSUES = ENDPOINT + '/issues?milestone={milestone}'
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
            raise CredentialsNotFoundError
        return func(*args, **kwargs)
    return inner

@authenticated
def fetch_milestones():
    """
    Retrieve the list of milestones for the getaround3 repository
    """
    auth = ('token', ACCESS_TOKEN)
    
    return requests.get(MILESTONES, auth=auth)

@authenticated
def fetch_issues_for_milestone(milestone_id):
    auth = ('token', ACCESS_TOKEN)
    endpoint = MILESTONE_ISSUES.format(milestone=milestone_id)

    return requests.get(endpoint, auth=auth)
