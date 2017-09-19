import collections
import json
import pprint

from collections import namedtuple

from zef import settings

from zef.facades import github_facade, zenhub_facade


DISPLAY = '{}\n\n'

ISSUE_ATTRIBUTES = [
    'url', 'repository_url', 'labels_url', 'comments_url',
    'events_url', 'html_url', 'id', 'number', 'title', 'user',
    'labels', 'state', 'locked', 'assignee', 'assignees', 'milestone',
    'comments', 'created_at', 'updated_at', 'closed_at', 'body', 'score',
    'pull_request', 'author_association'
]
Issue = collections.namedtuple('Issue', ISSUE_ATTRIBUTES)

MILESTONE_ATTRIBUTES = [
    'description', 'title', 'url', 'labels_url', 'created_at',
    'creator', 'number', 'html_url', 'updated_at', 'due_on',
    'state', 'closed_issues', 'open_issues', 'closed_at', 'id'
]
Milestone = collections.namedtuple('Milestone', MILESTONE_ATTRIBUTES)

def get_milestones():
    """
    Fetch all of the milestones for a given repository

    @rtype [Milestone]
    @return all milestones pertaining to repo
    """
    milestones = json.loads(github_facade.fetch_milestones().text)

    if not milestones:
        return

    return [Milestone(**milestone) for milestone in milestones]

def get_issues(milestone_id):
    """
    Fetch all of the issues for a given milestone

    @param int milestone_id: Identifier given by Github for milestone
    
    @rtype list
    @return all issues
    """
    # TODO: if no milestone_id is passed in, return all issues for the repo
    issues = json.loads(github_facade.fetch_issues_for_milestone(milestone_id).text)

    if not issues:
        return

    return [Issue(**issue) for issue in issues]

def display_milestones(milestones):
    display = ['%s %s' % (idx, milestone.title)
            for idx, milestone in enumerate(milestones, start=1)]
    return '\n'.join(display)

def ordered_milestones():
    milestones = get_milestones()
    milestones.sort(key=lambda m: m.title, reverse=True)
    return milestones

def create_test_fixture(fixture_filename, issues):
    """
    Write a file with the given issue information to be used for testing

    @param str fixture_filename: Name of the file to be created
    @param issues: Response of issue request
    """
    if fixture_filename:
        fixtures_file_path = settings.PROJECT_ROOT + '/tests/fixtures/' + fixture_filename + '.txt'
        with open(fixtures_file_path, 'w') as f:
            pretty_json = pprint.pprint(json.dumps(issues))
            f.write(pretty_json)

def get_search_issues(fixture_filename, verbose=False, **search):
    """
    Fetch issues given search key, value pairs
    """
    issues = json.loads(github_facade.fetch_search_issues(verbose=verbose, **search).text)
    create_test_fixture(fixture_filename, issues)

    items = issues.get('items')
    if not items:
        return

    results = []

    for attrs in items:
        # set all fields to None to allow for defaults
        Issue.__new__.__defaults__ = (None,) * len(Issue._fields)
        results.append(Issue(**attrs))

    return results

def issues_attr(issues, attr_name):
    """
    Helper method to access a given attribute for an iterable of Issue's

    @param list[Issue] issues: List instances to access
    @param str attr_name: Attribute that exists on each List item

    @return: Value of attribute from each List
    @rtype: list
    """
    results = []
    if not issues:
        return

    for issue in issues:
        value = getattr(issue, attr_name)
        if value:
            results.append(value)
    return results

def display_issues(milestone_id):
    issues = get_issues(milestone_id)
    return ''.join([DISPLAY.format(issue.body) for issue in issues.get("results")])

def search_issues(count=False, **search):
    issues = get_search_issues(**search)
    issues_display = ''.join([DISPLAY.format(issue.body) for issue in issues['results']])

    if count:
        issues_display += "Count: %s" % issues.get('count')

    return issues_display

def get_issue(issue_id, repo_id, verbose=False):
    response = zenhub_facade.fetch_issue(issue_id=issue_id, repo_id=repo_id, verbose=verbose)
    return json.loads(response.text)

def total_points_for_issues(issue_ids, repo_id, verbose=False):
    total = 0
    for issue_id in issue_ids:
        zenhub_issue = get_issue(issue_id=issue_id, repo_id=repo_id, verbose=verbose)
        if zenhub_issue.get('estimate'):
            # an issue can be created without an estimate
            total += zenhub_issue.get('estimate').get('value')
    return total

def get_repositories(name, verbose=False, **search):
    results = github_facade.fetch_repositories(repo_name=name, verbose=verbose, **search)
    return json.loads(results.text)

def repository_id(name, verbose=False, **search):
    results = get_repositories(name=name, verbose=verbose, **search)
    # TODO: what if a user wants to count issues across repos?
    if not results or results.get('total_count') > 1:
        return

    repo = results.get('items') and results.get('items')[0]
    # TODO: create a namedtuple that can be accessed by attributes
    return repo.get('id')

def total_points(fixture_filename, verbose=False, **search):
    """
    The total number of points for the issues
    @param str fixture_filename: Filename to persist for testing later
    @param bool verbose: Display helpful information for developers
    @param search: Keyword arguments used to search for issues
    """
    repo = search.get('repo')
    issues = get_search_issues(fixture_filename, verbose=verbose, **search)
    issue_ids = issues_attr(issues, 'number')
    if not issue_ids:
        return

    repo_id = repository_id(name=repo, verbose=verbose)
    return total_points_for_issues(issue_ids, repo_id, verbose=verbose)
    
