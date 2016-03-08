# Downloader

## Config

1. Install aria2c

2. Create file ```downloader/secret.py``` with this content:

        from .user import User

        team_city_user = User(username='your.name', password='your_pass')

3. Install requirements:

        pip install -r requirements.txt


## Usage

Run:

    python -m downloader URL
