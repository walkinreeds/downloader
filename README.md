# Downloader

## Config

Create file ```downloader/secret.py``` with this content:

    from .settings import User


    class TeamCityUser(User):
        username = 'your.username'
        password = 'your_password'

## Usage

Run:

    python -m downloader URL
