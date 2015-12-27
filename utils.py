import exifread
import os
from datetime import datetime

import settings


def get_dir_file_names(path):
    """
    A generator that returns an alphabetically ordered file names
    of a certain directory.

    :param path: a path to the directory
    :return: a tuple (file_name, full_file_name)
    """
    for file_name in sorted(os.listdir(path)):
        full_name = os.path.join(path, file_name)

        if os.path.isfile(full_name):
            yield file_name, full_name


def get_exif_datetime(file_name):
    """
    Reads and parses the EXIF datetime data of a give file_name and
    returns an appropriate datetime instance.

    :param file_name: a full filename of the picture
                      you need to get the EXIF data from
    :return: datetime instance or None
    """
    parsed_datetime = None

    with open(file_name, 'rb') as img_file:
        data = exifread.process_file(img_file)

        tag_datetime = data.get('EXIF DateTimeOriginal')

        if tag_datetime:
            parsed_datetime = datetime.strptime(
                str(tag_datetime),
                settings.EXIF_DATETIME_FORMAT
            )

    return parsed_datetime