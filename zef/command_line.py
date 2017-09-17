import click

from .services import issue_service, repository_service
from .interfaces import issues_interface


class Config(object):

    def __init__(self):
        self.selection = None


pass_config = click.make_pass_decorator(Config, ensure=True)

@click.group(name='cli')
@pass_config
def cli(config):
    pass

@cli.command()
@click.option('--verbose/--not-verbose', default=False, help='Show all requests being made')
@click.option('--fixture-filename', type=click.STRING, help='Save for fixture with given name')
@click.option('--repo', '-r', type=click.STRING, help='Specify repo for issues', required=True)
@click.option('--label', '-l', type=click.STRING, help='Search for issues by label')
@click.option('--assignee', '-a', type=click.STRING, help='Search for issues by username')
@click.option('--title', '-t', type=click.STRING, help='Search for issues by title')
@click.option('--milestone', '-m', type=click.STRING, help='Search for issues by milestone name')
def points(milestone, title, assignee, label, repo, fixture_filename, verbose=False):
    """
    Count of points from a given query

    Examples:

    Points for a user for a given sprint:

    $ zef --repo getaround/getaroun3 --assignee gkadillak --milestone web-128

    Total interrupts for a given sprint:

    $ zef --repo getaround/getaround3 --label interrupt
    """
    search = {}
    if assignee:
        search['assignee'] = assignee

    if title:
        search['title'] = title

    if milestone:
        search['milestone'] = milestone

    if label:
        search['label'] = label

    if repo:
        search['repo'] = repo

    issues = issue_service.get_search_issues(fixture_filename, verbose=verbose, **search)
    issue_ids = issue_service.issues_attr(issues, 'number')
    click.echo('Total points: %s' % issues_interface.total_points_for_issues(issue_ids, repo, verbose=verbose))

@cli.command()
@click.option('--fixture-filename', type=click.STRING, help='Save for fixture with given name')
@click.option('--repo', '-r', type=click.STRING, help='Specify repo for issues')
@click.option('--label', '-l', type=click.STRING, help='Search for issues by label')
@click.option('--assignee', '-a', type=click.STRING, help='Search for issues by username')
@click.option('--title', '-t', type=click.STRING, help='Search for issues by title')
@click.option('--milestone', '-m', type=click.STRING, help='Search for issues by milestone name')
def issues(milestone, title, assignee, label, repo, fixture_filename):
    pass

