"""Settings for aria2c"""

import os

from .secret import TeamCityUser

__all__ = ['Default', 'Recommended', ]


class User(object):
    username = str()
    password = str()


class Default(object):
    log = '-'
    dir = os.path.expanduser('~')
    out = None
    split = 5
    file_allocation = 'prealloc'
    file_allocation_values = ['none', 'prealloc', 'trunc', 'falloc']
    check_integrity = False
    continue_downloading = False
    input_file = None
    max_concurrent_downloads = 5
    force_sequential = False
    max_connection_per_server = 1
    min_split_size = 20971520
    ftp_user = None
    ftp_passwd = None
    http_user = None
    http_passwd = None
    load_cookies = None
    show_files = False
    max_overall_upload_limit = 0
    max_upload_limit = 0
    torrent_file = None
    listen_port = list(range(6881, 7000))
    enable_dht = True
    dht_listen_port = list(range(6881, 7000))
    enable_dht6 = False
    dht_listen_addr6 = None
    metalink_file = None


class Recommended(Default):
    dir = os.path.join(os.path.expanduser('~'), 'Downloads')
    split = 16
    file_allocation = 'falloc'
    max_concurrent_downloads = 16
    max_connection_per_server = 16
    min_split_size = 1048576
    enable_dht6 = True


class TeamCitySencha(Recommended):
    http_user = TeamCityUser.username
    http_passwd = TeamCityUser.password
