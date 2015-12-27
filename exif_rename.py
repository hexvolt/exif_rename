"""
EXIF rename tool.

Renames JPG files in a way to make them sorted by the date and time they were
actually taken. Useful for combining and sorting photos that were taken from
different devices. Has an ability to shift the EXIF data in order to adjust
the timezones or incorrect datetime settings of a certain device.

Usage:
  exif_rename.py <source> [--shifty <years>] [--shiftm <months>]
                          [--shifth <hours>] [-o | --overwrite-exif]
                          [-s | --save-name] [<destination>]
  exif_rename.py <source> ... (--info | -i)
  exif_rename.py (--help | -h)

Examples:
  exif_rename.py /home/admin/Pictures -i
            # show the EXIF datetime info about all pictures in a directory

  exif_rename.py /home/admin/Pictures --shifty +1
            # rename all the pictures in a directory according to EXIF datetime
            # data but with year increased by 1, EXIF data is not modified.

  exif_rename.py /home/admin/Pictures --shifth -3 -o /home/admin/temp
            # rename all the pictures of directory according to EXIF datetime
            # data, preliminarily decrease the time by 3 hours, and put the
            # result into .../temp directory. EXIF data will be also modified.

  exif_rename.py /home/admin/Pictures -s
            # rename all the pictures in a directory according to EXIF datetime
            # data and keep the original file name so the result will be like
            # `yyyymmdd_hhmmss(<original_name>).jpg`
Options:
  --shifty=<years>  Shift the EXIF-date's year when renaming the file
  --shiftm=<months> Shift the EXIF-date's month when renaming the file
  --shifth=<hours>  Shift the EXIF-date's hour when renaming the file
  -o --overwrite-exif  Overwrite the shifted date and time to file's EXIF data
  -s --save-name    Put the original file name into parenthesis
  -i --info         Show the EXIF data of the file(s)
  -h --help         Show this screen.
"""
import os
import logging

from docopt import docopt

from utils import get_exif_datetime


def show_pictures_info(path):
    """
    Displays the EXIF datetime info about all the pictures of a
    given directory.
    """
    path_msg = "\nEXIF date and time info of pictures in {} " \
               "(format: YYYY.MM.DD Hours:Minutes:Seconds):".format(path)

    print(path_msg)

    for file_name in sorted(os.listdir(path)):
        full_name = os.path.join(path, file_name)

        if not os.path.isfile(full_name):
            continue

        exif_datetime = get_exif_datetime(full_name)

        if not exif_datetime:
            continue

        formatted_exif = exif_datetime.strftime("%Y.%m.%d %H:%M:%S")

        print("{file}\t{exif}".format(file=file_name, exif=formatted_exif))


def rename_pictures():
    pass


def main():
    args = docopt(__doc__)

    sources = args.get('<source>')
    destination = args.get('<destination>')

    shift_year = args.get('--shifty')
    shift_month = args.get('--shiftm')
    shift_hour = args.get('--shifth')

    is_overwrite_exif = args.get('--overwrite-exif', False)
    is_save_name = args.get('--save-name', False)
    is_info = args.get('--info', False)

    if is_info:
        for path in sources:
            show_pictures_info(path)
        return

    rename_pictures()


if __name__ == '__main__':
    main()