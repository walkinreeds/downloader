"""Entry file for downloader"""

import sys

import click

from .aria2c import Aria2c
from .settings import Settings
from .secret import team_city_user

__all__ = ['main']


@click.command()
@click.argument('url', nargs=1, type=click.STRING)
def main(url):
    """Entry function for downloader

    Arguments:
        url (str): Download URL
    """
    settings = Settings('recommended')

    if url.startswith('https://'):
        if url[8:].startswith('teamcity.sencha.com/'):
            settings.http_user = team_city_user.username
            settings.http_passwd = team_city_user.password

    downloader = Aria2c()
    downloader.use_settings(settings)
    downloader.uri = url
    downloader.run()

if __name__ == '__main__':
    sys.exit(main())
