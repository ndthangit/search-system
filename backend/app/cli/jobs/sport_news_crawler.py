import asyncio
import subprocess

import click

from cli_scheduler.utils.parse_scheduler_utils import scheduler_format

from cli_scheduler import AsyncSchedulerJob

@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option(
    "--scheduler",
    default="^true@3600",
    show_default=True,
    type=str,
    help=f'Scheduler with format "{scheduler_format}"',
)
def sport_news_crawler(scheduler):
    job = SportNewsCrawler(scheduler=scheduler)
    asyncio.run(job.run())


class SportNewsCrawler(AsyncSchedulerJob):
    async def _start(self):
        self.logger.info("Start crawling sport news...")

    async def _execute(self, *args, **kwargs):
        subprocess.run([
            "scrapy",
            "crawl",
            "sport_news",
            "-o",
            "data/sport_news.jsonl",
            "-L",
            "INFO"
        ])

if __name__ == "__main__":
    sport_news_crawler()
