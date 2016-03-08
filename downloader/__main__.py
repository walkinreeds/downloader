"""Entry file for downloader"""

import sys

import click

from .aria2c import Aria2c
from .settings import TeamCitySencha

__all__ = ['main']


@click.command()
@click.argument('url', nargs=1, type=click.STRING)
def main(url):
    """Entry function for downloader

    Arguments:
        url (str): Download URL
    """
    downloader = Aria2c()
    downloader.use_settings(TeamCitySencha())
    downloader.uri = url
    downloader.run()

if __name__ == '__main__':
    sys.exit(main())
