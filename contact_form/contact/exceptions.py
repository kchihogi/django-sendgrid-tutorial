"""This module is for custom exceptions
"""

class NeedDBMasterException(Exception):
    def __init__(self, message):
        super().__init__(message)
