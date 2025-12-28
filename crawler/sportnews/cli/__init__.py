import click

from sportnews.cli.jobs.sport_news import sport_news_crawler


@click.group()
@click.version_option(version='1.0.0')
@click.pass_context
def cli(ctx):
    """Command line interface."""
    pass


@cli.group()
def updater():
    """Subcommands for Updater."""
    pass


cli.add_command(sport_news_crawler, "sport_news_crawler")