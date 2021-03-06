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
import shutil
import settings
from dateutil.relativedelta import relativedelta
from docopt import docopt

from utils import get_exif_datetime, get_dir_file_names, get_new_file_name


def show_pictures_info(path):
    """
    Displays the EXIF datetime info about all the pictures of a
    given directory.
    """
    path_msg = "\nEXIF date and time info of pictures in {} " \
               "(format: YYYY.MM.DD Hours:Minutes:Seconds):".format(path)

    print(path_msg)

    for file_name, full_name in get_dir_file_names(path):
        exif_datetime = get_exif_datetime(full_name)

        if not exif_datetime:
            continue

        formatted_exif = exif_datetime.strftime("%Y.%m.%d %H:%M:%S")

        print("{file}\t{exif}".format(file=file_name, exif=formatted_exif))


def rename_pictures(src_path, shift_year, shift_month, shift_hour,
                    is_overwrite_exif, is_save_name, destination_path=None):
    """
    Renames all the pictures of a src_path according to the EXIF date and time
    data taking into account the following options:

    :param src_path: a source directory where the target files are stored
    :param shift_year: <int> that represents the years-delta to be applied
                       before renaming
    :param shift_month: <int> that represents the months-delta to be applied
                        before renaming
    :param shift_hour: <float> that represents the hours-delta to be applied
                       before renaming
    :param is_overwrite_exif: if True, the original EXIF data will be
                              overwritten to the shifted one
    :param is_save_name: if True, the original file name will be mentioned
                         in the new file name
    :param destination_path: a path to the destination directory. If not
                             specified, the renaming will be performed on the
                             source files at the same directory
    """
    for file_name, full_name in get_dir_file_names(src_path):
        exif_datetime = get_exif_datetime(full_name)

        if not exif_datetime:
            continue

        # modifying exif_datetime according to specified options
        exif_datetime = exif_datetime + relativedelta(
            years=shift_year, months=shift_month, hours=shift_hour
        )

        # saving exif if need
        if is_overwrite_exif:
            pass

        # renaming
        new_name = get_new_file_name(file_name, exif_datetime, is_save_name)
        full_new_name = os.path.join(destination_path or src_path, new_name)

        if destination_path:
            shutil.copyfile(full_name, full_new_name)
        else:
            os.rename(full_name, full_new_name)


def main():
    args = docopt(__doc__)

    # parsing arguments
    sources = args.get('<source>')
    destination = args.get('<destination>')

    shift_year = args.get('--shifty')
    shift_month = args.get('--shiftm')
    shift_hour = args.get('--shifth')

    shift_year = int(shift_year) if shift_year else 0
    shift_month = int(shift_month) if shift_month else 0
    shift_hour = float(shift_hour) if shift_hour else 0

    is_info = args.get('--info', False)
    is_overwrite_exif = args.get('--overwrite-exif')
    is_save_name = args.get('--save-name')

    if is_info:
        for path in sources:
            show_pictures_info(path)
        return

    is_confirmed = True

    if not destination:
        # we should ask user for confirmation since in this case
        # we are going to change the files right in the source directory
        confirmation_msg = "WARNING: All the pictures of directory {} will " \
                           "be renamed and you won't be able to undo this " \
                           "operation. Continue? [Y/n]?".format(sources[0])
        is_confirmed = raw_input(confirmation_msg) not in ('n', 'N')

    elif not os.path.exists(destination):
        try:
            os.makedirs(destination)
        except OSError:
            print("Wrong destination directory. Please specify the right path")

    if is_confirmed:
        rename_pictures(
            src_path=sources[0],
            shift_year=shift_year,
            shift_month=shift_month,
            shift_hour=shift_hour,
            is_overwrite_exif=is_overwrite_exif,
            is_save_name=is_save_name,
            destination_path=destination
        )


if __name__ == '__main__':
    main()