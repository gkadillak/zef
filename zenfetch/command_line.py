import click

from .public import milestones, display_issues


class Config(object):

    def __init__(self):
        self.selection = None


pass_config = click.make_pass_decorator(Config, ensure=True)

@click.group(name='cli')
@pass_config
def cli(config):
    """Fetches tickets from Zenhub
    """
    pass

@cli.command()
@click.option('--username', '-u', type=click.STRING, help='Search for issues by username')
@click.option('--title', '-t', type=click.STRING, help='Search for issues by title')
@click.option('--milestone', '-m', type=click.STRING, help='Search for issues by milestone name')
def issues(username, title, milestone):
    # what's the best way to nest options?
    if username:
        click.echo(display_issues.search_issues(assignee=username))

    if title:
        click.echo('searching by title %s' % title)

    if milestone:
        return milestones.display
