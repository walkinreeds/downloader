"""Module for user handling"""

__all__ = ['User']


class User(object):
    """Class for user credentials"""
    def __init__(self, username=None, password=None):
        self._username = username
        self._password = password

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value
