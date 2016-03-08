# Downloader

## Config

1. Install aria2c

2. Clone the repo:

        git clone https://github.com/Sgiath/downloader.git && cd downloader

3. Create file ```downloader/secret.py``` with this content:

        from .user import User

        team_city_user = User(username='your.name', password='your_pass')

4. Install the program:

        pip install .

## Usage

Run:

    download URL
