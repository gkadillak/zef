from ..services import github_service

def display_issues(milestone_id):
    issues = github_service.get_issues(milestone_id)
    display = ""
    for issue in issues:
        display += "%s\n\n" % (issue.body)
    return display

