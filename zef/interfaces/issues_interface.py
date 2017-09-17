from ..services import repository_service, zenhub_service


def total_points_for_issues(issue_ids, repo, verbose):
    """
    Tally up the estimate count for the given issues
    
    @param list issue_ids: Id's for github issues
    @param str repo: Name of repository where the issues reside

    @return: Number of estimated points for the issues
    @rtype: int
    """
    if not issue_ids:
        return

    repo_id = repository_service.repository_id(name=repo, verbose=verbose)
    return zenhub_service.total_points_for_issues(issue_ids, repo_id, verbose=verbose)

def total_points_for_lane():
    pass
