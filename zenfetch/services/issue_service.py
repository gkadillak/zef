import collections
import json

from ..facades import github_facade

DISPLAY = '{}\n\n'


ISSUE_ATTRIBUTES = [
    'url', 'repository_url', 'labels_url', 'comments_url',
    'events_url', 'html_url', 'id', 'number', 'title', 'user',
    'labels', 'state', 'locked', 'assignee', 'assignees', 'milestone',
    'comments', 'created_at', 'updated_at', 'closed_at', 'body', 'score',
    'pull_request'
]

Issue = collections.namedtuple('Issue', ISSUE_ATTRIBUTES)


def get_search_issues(**search):
    """
    Fetch issues given search key, value pairs
    """
    issues = json.loads(github_facade.fetch_search_issues(**search).text)

    if not issues:
        return

    results = []
    for attrs in issues.get('items'):
        # set all fields to None to allow for defaults
        Issue.__new__.__defaults__ = (None,) * len(Issue._fields)
        results.append(Issue(**attrs))

    return {
        "count": issues.get("total_count"),
        "results": results
    }

def display_issues(milestone_id):
    issues = get_issues(milestone_id)
    return ''.join([DISPLAY.format(issue.body) for issue in issues.get("results")])

def search_issues(count=False, **search):
    issues = get_search_issues(**search)
    issues_display = ''.join([DISPLAY.format(issue.body) for issue in issues['results']])

    if count:
        issues_display += "Count: %s" % issues.get('count')

    return issues_display

