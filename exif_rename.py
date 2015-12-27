"""
EXIF rename tool.

Renames JPG files in a way to make them sorted by the date and time they were
actually taken. Useful for combining and sorting photos that were taken from
different devices. Has an ability to shift the EXIF data in order to adjust
the timezones or incorrect datetime settings of a certain device.

Usage:
  exif_rename.py <source> [--shifty <years>] [--shiftm <months>]
                          [--shifth <hours>] [--overwrite-exif | -o]
                          [<destination>]
  exif_rename.py <source> ... (--info | -i)
  exif_rename.py (--help | -h)

Examples:
  exif_rename.py /home/admin/Pictures -i
            # show the EXIF datetime of all pictures in a directory

  exif_rename.py /home/admin/Pictures --shifty +1
            # rename all the pictures in a directory according to EXIF datetime
            # data but with year increased by 1, EXIF data is not modified.

  exif_rename.py /home/admin/Pictures --shifth -3 -o /home/admin/temp
            # rename all the pictures of directory according to EXIF datetime
            # data, preliminarily decrease the time by 3 hours, and put the
            # result into .../temp directory. EXIF data will be also modified.

Options:
  --shifty=<years>  Shift the EXIF-date's year when renaming the file
  --shiftm=<months> Shift the EXIF-date's month when renaming the file
  --shifth=<hours>  Shift the EXIF-date's hour when renaming the file
  -o --overwrite-exif  Save the shifted date and time to file's EXIF data
  -i --info         Show the EXIF data of the file(s)
  -h --help         Show this screen.
"""
import os
import logging

from docopt import docopt

from utils import get_exif_datetime


def main():
    args = docopt(__doc__)

    sources = args.get('<source>')
    destination = args.get('<destination>')

    shift_year = args.get('--shifty')
    shift_month = args.get('--shiftm')
    shift_hour = args.get('--shifth')

    is_overwrite_exif = args.get('--overwrite-exif', False)
    is_info = args.get('--info', False)

if __name__ == '__main__':
    main()