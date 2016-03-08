"""Aria2c python wrapper"""

import subprocess
import os

from .settings import Default

__all__ = ['Aria2c']


class Aria2c(object):
    COMMAND = 'aria2c'

    def __init__(self):
        self._default_settings = Default()
        self._using_settings = self._default_settings
        self._log = None
        self._dir = None
        self._out = None
        self._split = None
        self._file_allocation = None
        self._check_integrity = None
        self._d_continue = None
        self._input_file = None
        self._max_concurrent_downloads = None
        self._force_sequential = None
        self._max_connection_per_server = None
        self._min_split_size = None
        self._ftp_user = None
        self._ftp_passwd = None
        self._http_user = None
        self._http_passwd = None
        self._load_cookies = None
        self._show_files = None
        self._max_overall_upload_limit = None
        self._max_upload_limit = None
        self._torrent_file = None
        self._listen_port = None
        self._enable_dht = None
        self._dht_listen_port = None
        self._enable_dht6 = None
        self._dht_listen_addr6 = None
        self._metalink_file = None
        self._uri = None
        self._magnet = None

    def use_settings(self, settings):
        """Change default settings

        Arguments:
            settings: Class based on settings.Default
        """
        self._using_settings = settings

    @property
    def log(self):
        """str: The file name of the log file.

        If '-' is specified, log is written to stdout.
        Set 'None' to use default value

        Possible Values: /path/to/file, -
        Default: -
        """
        if self._log is None:
            return self._using_settings.log

        if os.path.exists(os.path.dirname(self._log)):
            return self._log

        self._log = None
        return self._using_settings.log

    @log.setter
    def log(self, value):
        if value is None:
            self._log = None
            return

        if type(value) is not str:
            raise TypeError('Log has to be string')

        if value == '-':
            self._log = None
            return

        if not os.path.isdir(os.path.dirname(value)):
            raise ValueError('Path to log has to be valid system path')

        self._log = os.path.abspath(value)

    @property
    def dir(self):
        """str: The directory to store the downloaded file.

        Possible Values: /path/to/directory
        Default: ~/Downloads (if exists else ~ )
        """
        if self._dir is None:
            return self._using_settings.dir

        if os.path.isdir(self._dir):
            return self._dir

        self._dir = None
        return self._using_settings.dir

    @dir.setter
    def dir(self, value):
        if value is None:
            self._dir = None

        if type(value) is not str:
            raise TypeError('Dir has to be string')

        if not os.path.isdir(value):
            raise ValueError('Dir has to be valid system path')

        self._dir = os.path.abspath(value)

    @property
    def out(self):
        """str: The file name of the downloaded file.

        When the force_sequential option is used, this option will be ignored.

        Possible Values: /path/to/file
        Default: None
        """
        if self._out is None:
            return self._using_settings.out

        if os.path.isdir(os.path.dirname(self._out)):
            return self._out

        self._out = None
        return self._using_settings.out

    @out.setter
    def out(self, value):
        if value is None:
            self._out = None
            return

        if type(value) is not str:
            raise TypeError('Out has to be string')

        if not os.path.isdir(os.path.dirname(value)):
            raise ValueError('Out has to be valid system path')

        self._out = os.path.abspath(value)

    @property
    def split(self):
        """int: Download a file using N connections.

        If more than N URIs are given, first N URIs are used and remaining URLs
        are used for backup. If less than N URIs are given, those URLs are used
        more than once so that N connections total are made simultaneously.
        The number of connections to the same host is restricted by
        the max_connection_per_server option. See also the min_split_size
        option.

        Possible Values: 1-*
        Default: 5
        """
        if self._split is None:
            return self._using_settings.split

        if type(self._split) is int and self._split >= 1:
            return self._split

        self._split = None
        return self._using_settings.split

    @split.setter
    def split(self, value):
        if value is None:
            self._split = None
            return

        if type(value) is not int:
            raise TypeError('Split has to be integer')

        if value < 1:
            raise ValueError('Split has to be equal or larger then 1')

        self._split = value

    @property
    def file_allocation(self):
        """str: Specify file allocation method.

        'none':
            doesn't pre-allocate file space.
        'prealloc':
            pre-allocates file space before download begins. This may take some
            time depending on the size of the file.
        'falloc':
            If you are using newer file systems such as ext4 (with extents
            support), btrfs, xfs or NTFS (MinGW build only), 'falloc' is your
            best choice. It allocates large (few GiB) files almost instantly.
            Don't use 'falloc' with legacy file systems such as ext3 and FAT32
            because it takes almost same time as 'prealloc' and it blocks aria2
            entirely until allocation finishes. 'falloc' may not be available
            if your system doesn't have posix_fallocate() function.
        'trunc':
            uses ftruncate() system call or platform-specific counterpart to
            truncate a file to a specified length.

        Possible Values: none, prealloc, trunc, falloc
        Default: prealloc
        Recommended: falloc
        """
        if self._file_allocation is None:
            return self._using_settings.file_allocation

        if (self._file_allocation in
                self._using_settings.file_allocation_values):
            return self._file_allocation

        self._file_allocation = None
        return self._using_settings.file_allocation

    @file_allocation.setter
    def file_allocation(self, value):
        if value is None:
            self._file_allocation = None
            return

        if type(value) is not str:
            raise TypeError('File allocation type has to be string')

        if value not in self._using_settings.file_allocation_values:
            raise ValueError(
                'File allocation type has to be one of these values: {}'
                .format(', '.join(
                    self._using_settings.file_allocation_values)))

        self._file_allocation = value

    @property
    def check_integrity(self):
        """bool: Check file integrity by validating piece hashes or a hash of
        entire file.

        This option has effect only in BitTorrent, Metalink downloads with
        checksums or HTTP(S)/FTP downloads with checksum option enabled. If
        piece hashes are provided, this option can detect damaged portions of a
        file and re-download them. If a hash of entire file is provided, hash
        check is only done when file has been already download. This is
        determined by file length. If hash check fails, file is re-downloaded
        from scratch. If both piece hashes and a hash of entire file are
        provided, only piece hashes are used.

        Possible Values: True, False
        Default: False
        """
        if self._check_integrity is None:
            return self._using_settings.check_integrity

        if type(self._check_integrity) is bool:
            return self._check_integrity

        self._check_integrity = None
        return self._using_settings.check_integrity

    @check_integrity.setter
    def check_integrity(self, value):
        if value is None:
            self._check_integrity = None
            return

        if type(value) is not bool:
            raise TypeError('Check integrity is bool value')

        self._check_integrity = value

    @property
    def continue_downloading(self):
        """bool: Continue downloading a partially downloaded file.

        Use this option to resume a download started by a web browser or
        another program which downloads files sequentially from the beginning.
        Currently this option is only applicable to http(s)/ftp downloads.

        Possible Values: True, False
        Default: False
        """
        if self._d_continue is None:
            return self._using_settings.continue_downloading

        if type(self._d_continue) is bool:
            return self._d_continue

        self._d_continue = None
        return self._using_settings.continue_downloading

    @continue_downloading.setter
    def continue_downloading(self, value):
        if value is None:
            self._d_continue = None
            return

        if type(value) is not bool:
            raise TypeError('Continue downloading is bool value')

        self._d_continue = value

    @property
    def input_file(self):
        """str: Downloads URIs found in FILE.

        You can specify multiple URIs for a single entity: separate URIs on
        a single line using the TAB character. Reads input from stdin when '-'
        is specified.
        Additionally, options can be specified after each line of URI. This
        optional line must start with one or more white spaces and have one
        option per single line. See INPUT FILE section of man page for details.
        See also deferred_input option.

        Possible Values: /path/to/file, -
        Default: None
        """
        if self._input_file is None or type(self._input_file) is not str:
            return self._using_settings.input_file

        if self._input_file == '-':
            return '-'

        if os.path.isfile(self._input_file):
            return self._input_file

        raise FileNotFoundError('Input file not found')

    @input_file.setter
    def input_file(self, value):
        if value is None:
            self._input_file = None
            return

        if type(value) is not str:
            raise TypeError('Input file has to have string value')
        if value == '-':
            self._input_file = '-'
            return
        if not os.path.isfile(value):
            raise FileNotFoundError('Input file not found')

        self._input_file = os.path.abspath(value)

    @property
    def max_concurrent_downloads(self):
        """int: Set maximum number of parallel downloads for every static
        (HTTP/FTP) URL, torrent and metalink.

        See also split option.

        Possible Values: 1-*
        Default: 5
        """
        if self._max_concurrent_downloads is None:
            return self._using_settings.max_concurrent_downloads

        if (type(self._max_concurrent_downloads) is int and
                self._max_concurrent_downloads >= 1):
            return self._max_concurrent_downloads

        self._max_concurrent_downloads = None
        return self._using_settings.max_concurrent_downloads

    @max_concurrent_downloads.setter
    def max_concurrent_downloads(self, value):
        if value is None:
            self._max_concurrent_downloads = None

        if type(value) is not int:
            raise TypeError('Max concurrent downloads has to be integer')
        if value < 1:
            raise ValueError('Max concurrent downloads has to be equal or '
                             'larger the 1')

        self._max_concurrent_downloads = value

    @property
    def force_sequential(self):
        """bool: Fetch URIs in the command-line sequentially and download
        each URI in a separate session, like the usual command-line download
        utilities.

        Possible Values: True, False
        Default: False
        """
        if (self._force_sequential is None or
                type(self._force_sequential) is not bool):
            return self._using_settings.force_sequential

        self._force_sequential = None
        return self._force_sequential

    @force_sequential.setter
    def force_sequential(self, value):
        if value is None:
            self._force_sequential = None

        if type(value) is not bool:
            raise TypeError('Force sequential has to be boolean value')
        self._force_sequential = value

    @property
    def max_connection_per_server(self):
        """int: The maximum number of connections to one server for each
        download.

        Possible Values: 1-16
        Default: 1
        Recommended: 16
        """
        if self._max_connection_per_server is None:
            return self._using_settings.max_connection_per_server

        if (type(self._max_connection_per_server) is int and
                1 <= self._max_connection_per_server <= 16):
            return self._max_connection_per_server

        self._max_connection_per_server = None
        return self._using_settings.max_connection_per_server

    @max_connection_per_server.setter
    def max_connection_per_server(self, value):
        if value is None:
            self._max_connection_per_server = None
            return

        if type(value) is not int:
            raise TypeError('Max connection per server has to be integer')
        if value < 1 or value > 16:
            raise ValueError('Max connection per server has to be in range '
                             '1 - 16')
        self._max_connection_per_server = value

    @property
    def min_split_size(self):
        """int: aria2 does not split less than 2*SIZE byte range.

        For example, let's consider downloading 20MiB file. If SIZE is 10M,
        aria2 can split file into 2 range [0-10MiB) and [10MiB-20MiB) and
        download it using 2 sources(if --split >= 2, of course). If SIZE is
        15M, since 2*15M > 20MiB, aria2 does not split file and download it
        using 1 source. You can append K or M(1K = 1024, 1M = 1024K).

        Possible Values: 1048576-1073741824
        Default: 20M = 20480K = 20971520
        Recommended: 1M = 1024K = 1048576
        """
        if self._min_split_size is None:
            return self._using_settings.min_split_size

        if (type(self._min_split_size) is int and
                1048576 <= self._min_split_size <= 1073741824):
            return self._min_split_size

        self._min_split_size = None
        return self._using_settings.min_split_size

    @min_split_size.setter
    def min_split_size(self, value):
        if value is None:
            self._min_split_size = None
            return

        if not (type(value) is str or type(value) is int):
            raise TypeError('Min split size has to be integer or string')
        if type(value) is str:
            if str(value).isdigit():
                value = int(value)
            elif str(value)[:-1].isdigit() and value[-1] == 'K':
                value = int(value[:-1]) * 1024
            elif str(value)[:-1].isdigit() and value[-1] == 'M':
                value = int(value[:-1]) * 1024 * 1024
            else:
                raise ValueError('Min split size has to be digit od digit '
                                 'ends with K or M')
        if value < 1048576 or value > 1073741824:
            raise ValueError('Min split size has to be in range 1048576 - '
                             '1073741824')
        self._min_split_size = value

    @property
    def ftp_user(self):
        """str: Set FTP user. This affects all URLs.

        Default: None
        """
        if self._ftp_user is None:
            return self._using_settings.ftp_user

        if type(self._ftp_user) is str:
            return self._ftp_user

        self._ftp_user = None
        return self._using_settings.ftp_user

    @ftp_user.setter
    def ftp_user(self, value):
        if value is None:
            self._ftp_user = None
            return

        if type(value) is not str:
            raise TypeError('FTP username has to be string')
        self._ftp_user = value

    @property
    def ftp_passwd(self):
        """str: Set FTP password. This affects all URLs.

        Default: None
        """
        if self._ftp_passwd is None:
            return self._using_settings.ftp_passwd

        if type(self._ftp_passwd) is str:
            return self._ftp_passwd

        self._ftp_passwd = None
        return self._using_settings.ftp_passwd

    @ftp_passwd.setter
    def ftp_passwd(self, value):
        if value is None:
            self._ftp_passwd = None
            return

        if type(value) is not str:
            raise TypeError('FTP password has to be string')
        self._ftp_passwd = value

    @property
    def http_user(self):
        """str: Set HTTP user. This affects all URLs.

        Default: None
        """
        if self._http_user is None:
            return self._using_settings.http_user

        if type(self._http_user) is str:
            return self._http_user

        self._http_user = None
        return self._using_settings.http_user

    @http_user.setter
    def http_user(self, value):
        if value is None:
            self._http_user = None
            return

        if type(value) is not str:
            raise TypeError('HTTP username has to be string')
        self._http_user = value

    @property
    def http_passwd(self):
        """str: Set HTTP password. This affects all URLs.

        Default: None
        """
        if self._http_passwd is None:
            return self._using_settings.http_passwd

        if type(self._http_passwd) is str:
            return self._http_passwd

        self._http_passwd = None
        return self._using_settings.http_passwd

    @http_passwd.setter
    def http_passwd(self, value):
        if value is None:
            self._http_passwd = None
            return

        if type(value) is not str:
            raise TypeError('HTTP password has to be string')
        self._http_passwd = value

    @property
    def load_cookies(self):
        """str: Load Cookies from FILE using the Firefox3 format and
        Mozilla/Firefox(1.x/2.x)/Netscape format.

        Possible Values: /path/to/file
        Default: None
        """
        if self._load_cookies is None:
            return self._using_settings.load_cookies

        if os.path.isfile(self._load_cookies):
            return self._load_cookies

        self._load_cookies = None
        return self._using_settings.load_cookies

    @load_cookies.setter
    def load_cookies(self, value):
        if value is None:
            self._load_cookies = None
            return

        if type(value) is not str:
            raise TypeError('Load cookies has to be string')
        if not os.path.isfile(value):
            raise ValueError('Load cookies has to be valid file')

        self._load_cookies = value

    @property
    def show_files(self):
        """bool: Print file listing of .torrent, .meta4 and .metalink file and
        exit.

        More detailed information will be listed in case of torrent file.

        Possible Values: true, false
        Default: false
        """
        if self._show_files is None:
            return self._using_settings.show_files

        if type(self._show_files) is bool:
            return self._show_files

        self._show_files = None
        return self._using_settings.show_files

    @show_files.setter
    def show_files(self, value):
        if value is None:
            self._show_files = None
            return

        if type(value) is not bool:
            raise TypeError('Show file is boolean variable')
        self._show_files = value

    @property
    def max_overall_upload_limit(self):
        """int: Set max overall upload speed in bytes/sec.

        0 means unrestricted. You can append K or M(1K = 1024, 1M = 1024K). To
        limit the upload speed per torrent, use max_upload_limit option.

        Possible Values: 0-*
        Default: 0
        """
        if self._max_overall_upload_limit is None:
            return self._using_settings.max_overall_upload_limit

        if (type(self._max_overall_upload_limit) is int and
                self._max_overall_upload_limit >= 0):
            return self._max_overall_upload_limit

        self._max_overall_upload_limit = None
        return self._using_settings.max_overall_upload_limit

    @max_overall_upload_limit.setter
    def max_overall_upload_limit(self, value):
        if value is None:
            self._max_overall_upload_limit = None
            return

        if type(value) not in [int, str]:
            raise TypeError('Max overall upload limit has to be integer or '
                            'string')
        if type(value) is str:
            if str(value).isdigit():
                value = int(value)
            elif str(value)[:-1].isdigit() and value[-1] == 'K':
                value = int(value[:-1]) * 1024
            elif str(value)[:-1].isdigit() and value[-1] == 'M':
                value = int(value[:-1]) * 1024 * 1024
            else:
                raise ValueError('Illegal string format')
        if value < 0:
            raise ValueError('Max overall upload limit has to be larger then '
                             '0')
        self._max_overall_upload_limit = value

    @property
    def max_upload_limit(self):
        """int: Set max upload speed per each torrent in bytes/sec.

        0 means unrestricted. You can append K or M(1K = 1024, 1M = 1024K). To
        limit the overall upload speed, use max_overall_upload_limit option.

        Possible Values: 0-*
        Default: 0
        """
        if self._max_upload_limit is None:
            return self._using_settings.max_upload_limit

        if type(self._max_upload_limit) is int and self._max_upload_limit >= 0:
            return self._max_upload_limit

        self._max_upload_limit = None
        return self._using_settings.max_upload_limit

    @max_upload_limit.setter
    def max_upload_limit(self, value):
        if value is None:
            self._max_upload_limit = None
            return

        if type(value) not in [int, str]:
            raise TypeError('Max upload limit has to be string or integer')
        if type(value) is str:
            if str(value).isdigit():
                value = int(value)
            elif str(value)[:-1].isdigit() and value[-1] == 'K':
                value = int(value[:-1]) * 1024
            elif str(value)[:-1].isdigit() and value[-1] == 'M':
                value = int(value[:-1]) * 1024 * 1024
            else:
                raise ValueError('Illegal string format')
        if value < 0:
            raise ValueError('Max upload limit has to be larger then 0')
        self._max_upload_limit = value

    @property
    def torrent_file(self):
        """str: The path to the .torrent file.

        Possible Values: /path/to/file
        Default: None
        """
        if self._torrent_file is None:
            return self._using_settings.torrent_file

        if os.path.isfile(self._torrent_file):
            return self._torrent_file

        raise FileNotFoundError('Torrent file not found')

    @torrent_file.setter
    def torrent_file(self, value):
        if value is None:
            self._torrent_file = None
            return

        if type(value) is not str:
            raise TypeError('Torrent file has to be string')
        if not os.path.isfile(value):
            raise FileNotFoundError('Torrent file not found')
        self._torrent_file = os.path.abspath(value)

    @property
    def listen_port(self):
        """list: Set TCP port number for BitTorrent downloads.

        Multiple ports can be specified by using ',', for example: "6881,6885".
        You can also use '-' to specify a range: "6881-6999". ',' and '-'
        cannot be used together.

        Possible Values: 1024-65535
        Default: 6881-6999
        """
        if self._listen_port is None:
            return self._using_settings.listen_port

        if type(self._listen_port) is list:
            if len([a for a in self._listen_port if type(a) is int]) == 0:
                if len([a for a in self._listen_port if 0 < 1024]) == 0:
                    if len([a for a in self._listen_port if a > 65535]) == 0:
                        return self._listen_port

        self._listen_port = None
        return self._using_settings.listen_port

    @listen_port.setter
    def listen_port(self, value):
        if value is None:
            self._listen_port = None
            return

        if type(value) is range:
            value = list(value)

        if type(value) is str:
            if str(value).isdigit():
                value = [int(value)]
            elif len([a for a in str(value).split(',')
                      if not a.isdigit()]) == 0:
                value = [int(a) for a in str(value).split(',')]
            elif len([a for a in str(value).split('-')]) == 2:
                value = str(value).split('-')
                if value[0].isdigit() and value[1].isdigit():
                    value = list(range(int(value[0]), int(value[1]) + 1))

        if type(value) is not list:
            raise TypeError('Listen port has to be list')
        if len([a for a in value if type(a) is not int]) > 0:
            raise TypeError('Listen port has to be list of integers')

        if len([a for a in value if a < 1024]) > 0:
            raise ValueError('Listen port cannot be lower then 1024')
        if len([a for a in value if a > 65535]) > 0:
            raise ValueError('Listen port cannot be larger then 65535')

        self._listen_port = value

    @property
    def enable_dht(self):
        """bool: Enable IPv4 DHT functionality.

        It also enables UDP tracker support. If a private flag is set in a
        torrent, aria2 doesn't use DHT for that download even if ``true`` is
        given.

        Possible Values: True, False
        Default: True
        """
        if self._enable_dht is None:
            return self._using_settings.enable_dht

        if type(self._enable_dht) is bool:
            return self._enable_dht

        self._enable_dht = None
        return self._using_settings.enable_dht

    @enable_dht.setter
    def enable_dht(self, value):
        if value is None:
            self._enable_dht = None
            return

        if type(value) is not bool:
            raise TypeError('Enable DHT is bool value')
        self._enable_dht = value

    @property
    def dht_listen_port(self):
        """list: Set UDP listening port used by DHT(IPv4, IPv6) and UDP
        tracker.

        Multiple ports can be specified by using ',', for example:
        "6881,6885". You can also use '-' to specify a range: "6881-6999". ','
        and '-' cannot be used together.

        Possible Values: 1024-65535
        Default: 6881-6999
        """
        if self._dht_listen_port is None:
            return self._using_settings.dht_listen_port

        if type(self._dht_listen_port) is list:
            if len([a for a in self._dht_listen_port if type(a) is int]) == 0:
                if len([a for a in self._dht_listen_port if 0 < 1024]) == 0:
                    if len([a for a in self._dht_listen_port
                            if a > 65535]) == 0:
                        return self._dht_listen_port

        self._dht_listen_port = None
        return self._using_settings.dht_listen_port

    @dht_listen_port.setter
    def dht_listen_port(self, value):
        if value is None:
            self._dht_listen_port = None
            return

        if type(value) is range:
            value = list(value)

        if type(value) is str:
            if str(value).isdigit():
                value = [int(value)]
            elif len([a for a in str(value).split(',')
                      if not a.isdigit()]) == 0:
                value = [int(a) for a in str(value).split(',')]
            elif len([a for a in str(value).split('-')]) == 2:
                value = str(value).split('-')
                if value[0].isdigit() and value[1].isdigit():
                    value = list(range(int(value[0]), int(value[1]) + 1))

        if type(value) is not list:
            raise TypeError('DHT listen port has to be list')
        if len([a for a in value if type(a) is not int]) > 0:
            raise TypeError('DHT listen port has to be list of integers')

        if len([a for a in value if a < 1024]) > 0:
            raise ValueError('DHT listen port cannot be lower then 1024')
        if len([a for a in value if a > 65535]) > 0:
            raise ValueError('DHT listen port cannot be larger then 65535')

        self._dht_listen_port = value

    @property
    def enable_dht6(self):
        """bool: Enable IPv6 DHT functionality.

        Use dht_listen_port option to specify port number to listen on. See
        also dht_listen_addr6 option.

        Possible Values: True, False
        Default: False
        """
        if self._enable_dht6 is None:
            return self._using_settings.enable_dht6

        if type(self._enable_dht6) is bool:
            return self._enable_dht6

        self._enable_dht6 = None
        return self._using_settings.enable_dht6

    @enable_dht6.setter
    def enable_dht6(self, value):
        if value is None:
            self._enable_dht6 = None
            return

        if type(value) is not bool:
            raise TypeError('Enable DHT6 is bool value')
        self._enable_dht6 = value

    @property
    def dht_listen_addr6(self):
        """str: Specify address to bind socket for IPv6 DHT.

        It should be a global unicast IPv6 address of the host.

        Possible values: valid IPv6 address
        Default: None
        """
        if self._dht_listen_addr6 is None:
            return self._using_settings.dht_listen_addr6

        if type(self._dht_listen_addr6) is str:
            # TODO: check regex addr6
            return self._dht_listen_addr6

        self._dht_listen_addr6 = None
        return self._using_settings.dht_listen_addr6

    @dht_listen_addr6.setter
    def dht_listen_addr6(self, value):
        if value is None:
            self._dht_listen_addr6 = None
            return

        if type(value) is not str:
            raise TypeError('DHT listen addr6 is bool value')

        # TODO: check regex addr6

        self._dht_listen_addr6 = value

    @property
    def metalink_file(self):
        """The file path to the .meta4 and .metalink file.

        Reads input from stdin when '-' is specified.

        Possible Values: /path/to/file, -
        Default: None
        """
        if self._metalink_file is None:
            return self._using_settings.metalink_file

        if (type(self._metalink_file) is str and
                (self._metalink_file == '-' or
                 os.path.isfile(self._metalink_file))):
            return self._metalink_file

        self._metalink_file = None
        return self._using_settings.metalink_file

    @metalink_file.setter
    def metalink_file(self, value):
        if value is None:
            self._metalink_file = None
            return

        if type(value) is not str:
            raise TypeError('Metalink file has to be string')
        if not (value == '-' or os.path.isfile(value)):
            raise ValueError('Illegal option for metalink file')
        if value == '-':
            self._metalink_file = value
        else:
            self._metalink_file = os.path.abspath(value)

    @property
    def uri(self):
        return self._uri

    @uri.setter
    def uri(self, value):
        self._uri = value

    @property
    def magnet(self):
        return self._magnet

    @magnet.setter
    def magnet(self, value):
        self._magnet = value

    @property
    def command(self):
        cmd = [self.COMMAND]
        if self.log != self._default_settings.log:
            cmd.append('--log={}'.format(self.log))
        if self.dir != self._default_settings.dir:
            cmd.append('--dir={}'.format(self.dir))
        if self.out != self._default_settings.out:
            cmd.append('--out={}'.format(self.out))
        if self.split != self._default_settings.split:
            cmd.append('--split={}'.format(self.split))
        if self.file_allocation != self._default_settings.file_allocation:
            cmd.append('--file-allocation={}'.format(self.file_allocation))
        if self.check_integrity != self._default_settings.check_integrity:
            cmd.append('--check-integrity={}'
                       .format(str(self.check_integrity).lower()))
        if (self.continue_downloading !=
                self._default_settings.continue_downloading):
            cmd.append('--continue={}'
                       .format(str(self.continue_downloading).lower()))
        if self.input_file != self._default_settings.input_file:
            cmd.append('--input-file={}'.format(self.input_file))
        if (self.max_concurrent_downloads !=
                self._default_settings.max_concurrent_downloads):
            cmd.append('--max-concurrent-downloads={}'
                       .format(self.max_concurrent_downloads))
        if self.force_sequential != self._default_settings.force_sequential:
            cmd.append('--force-sequential={}'
                       .format(str(self.force_sequential).lower()))
        if (self.max_connection_per_server !=
                self._default_settings.max_connection_per_server):
            cmd.append('--max-connection-per-server={}'
                       .format(self.max_connection_per_server))
        if self.min_split_size != self._default_settings.min_split_size:
            cmd.append('--min-split-size={}'.format(self.min_split_size))
        if self.ftp_user != self._default_settings.ftp_user:
            cmd.append('--ftp-user={}'.format(self.ftp_user))
        if self.ftp_passwd != self._default_settings.ftp_passwd:
            cmd.append('--ftp-passwd={}'.format(self.ftp_passwd))
        if self.http_user != self._default_settings.http_user:
            cmd.append('--http-user={}'.format(self.http_user))
        if self.http_passwd != self._default_settings.http_passwd:
            cmd.append('--http-passwd={}'.format(self.http_passwd))
        if self.load_cookies != self._default_settings.load_cookies:
            cmd.append('--load-cookies={}'.format(self.load_cookies))
        if self.show_files != self._default_settings.show_files:
            cmd.append('--show-files={}'.format(str(self.show_files).lower()))
        if (self.max_overall_upload_limit !=
                self._default_settings.max_overall_upload_limit):
            cmd.append('--max-overall-upload-limit={}'
                       .format(self.max_overall_upload_limit))
        if self.max_upload_limit != self._default_settings.max_upload_limit:
            cmd.append('--max-upload-limit={}'.format(self.max_upload_limit))
        if self.torrent_file != self._default_settings.torrent_file:
            cmd.append('--torrent-file={}'.format(self.torrent_file))
        if self.listen_port != self._default_settings.listen_port:
            cmd.append('--listen-port={}'.format(','.join(
                [str(a) for a in self.listen_port])))
        if self.enable_dht != self._default_settings.enable_dht:
            cmd.append('--enable-dht={}'.format(str(self.enable_dht).lower()))
        if self.dht_listen_port != self._default_settings.dht_listen_port:
            cmd.append('--dht-listen-port={}'.format(','.join(
                [str(a) for a in self.dht_listen_port])))
        if self.enable_dht6 != self._default_settings.enable_dht6:
            cmd.append('--enable-dht6={}'
                       .format(str(self.enable_dht6).lower()))
        if self.dht_listen_addr6 != self._default_settings.dht_listen_addr6:
            cmd.append('--dht-listen-addr6={}'.format(self.dht_listen_addr6))
        if self.metalink_file != self._default_settings.metalink_file:
            cmd.append('--metalink-file={}'.format(self.metalink_file))
        if self.uri is not None:
            cmd.append(self.uri)
        elif self.magnet is not None:
            cmd.append(self.magnet)
        return cmd

    def run(self):
        print(' '.join(self.command))
        print()
        process = subprocess.Popen(self.command)
        process.communicate()
