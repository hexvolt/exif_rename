"""
CLI to the Bed Crawler Scrapy daemon.

Usage:
  exif_rename.py <source> ... [--shifty <years>] [--shiftm <months>] [--shifth <hours>] <destination>
  exif_rename.py <source> ... (--info | -i)

"""
import os
import logging

from docopt import docopt

from utils import get_exif_datetime


def main():
    pass

if __name__ == '__main__':
    main()