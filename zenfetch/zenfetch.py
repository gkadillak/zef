import click

from .public import milestones


class Config(object):

    def __init__(self):
        self.selection = None


pass_config = click.make_pass_decorator(Config, ensure=True)

@click.command()
@pass_config
def cli(config):
    """Fetches tickets from Zenhub
    """
    def pick_milestone():
        config.selection = click.prompt("Enter the milestone's number", type=int)

    ordered_milestones = milestones.ordered()

    click.echo(milestones.display(ordered_milestones))

    pick_milestone()
    
    while not (0 < config.selection <= len(ordered_milestones)):
        # bad user! pick again!
        pick_milestone()

    ordered_milestones[config.selection - 1])


# zfetch issues count -i
