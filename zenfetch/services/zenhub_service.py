import json

from ..facades import zenhub_facade

def get_issue(issue_id, repo_id):
    response = zenhub_facade.fetch_issue(issue_id=issue_id, repo_id=repo_id)
    return json.loads(response.text)


def total_points_for_issues(issue_ids, repo_id):
    total = 0
    for issue_id in issue_ids:
        zenhub_issue = get_issue(issue_id=issue_id, repo_id=repo_id)
        if zenhub_issue.get('estimate'):
            # an issue can be created without an estimate
            total += zenhub_issue.get('estimate').get('value')
    return total
