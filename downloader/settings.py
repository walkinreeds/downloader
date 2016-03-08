"""Settings for aria2c"""

import os

__all__ = ['Settings']


class Settings(object):
    def __init__(self, use='default'):
        self.log = '-'
        self.dir = os.path.expanduser('~')
        self.out = None
        self.split = 5
        self.file_allocation = 'prealloc'
        self.file_allocation_values = ['none', 'prealloc', 'trunc',
                                       'falloc']
        self.check_integrity = False
        self.continue_downloading = False
        self.input_file = None
        self.max_concurrent_downloads = 5
        self.force_sequential = False
        self.max_connection_per_server = 1
        self.min_split_size = 20971520
        self.ftp_user = None
        self.ftp_passwd = None
        self.http_user = None
        self.http_passwd = None
        self.load_cookies = None
        self.show_files = False
        self.max_overall_upload_limit = 0
        self.max_upload_limit = 0
        self.torrent_file = None
        self.listen_port = list(range(6881, 7000))
        self.enable_dht = True
        self.dht_listen_port = list(range(6881, 7000))
        self.enable_dht6 = False
        self.dht_listen_addr6 = None
        self.metalink_file = None

        if use == 'recommended':
            self.dir = os.path.join(os.path.expanduser('~'), 'Downloads')
            self.split = 16
            self.file_allocation = 'falloc'
            self.max_concurrent_downloads = 16
            self.max_connection_per_server = 16
            self.min_split_size = 1048576
            self.enable_dht6 = True
