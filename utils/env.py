import sys
from os import getenv

DEBUG = getenv("DEBUG", "1")
EXPORT_PATH = getenv("EXPORT_PATH", "output")
IS_FROZEN = getattr(sys, 'frozen', False)


def is_debug():
    return DEBUG == '1'


def is_release():
    return DEBUG == '0'
