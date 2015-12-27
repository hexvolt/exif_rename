import datetime
import os

import exifread

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
            parsed_datetime = datetime.datetime.strptime(
                str(tag_datetime),
                settings.EXIF_DATETIME_FORMAT
            )

    return parsed_datetime


def get_new_file_name(original_file_name, exif_datetime, is_save_name=None):
    """
    Composes a new file name of the picture based on its EXIF data
    and is_save_name option. The result doesn't contain a path to the file
    as well as the function arguments.

    :param original_file_name: a name of the original file (without path)
    :param exif_datetime: a datetime instance retrieved from EXIF data
    :param is_save_name: if True - a name of the original file will be
                         attached in the parenthesis
    :return: a new name of the given file
    """
    base_name, extension = os.path.splitext(original_file_name)

    new_base_name = exif_datetime.strftime(settings.NEW_BASENAME_FORMAT)

    if is_save_name:
        new_base_name += '({})'.format(base_name)

    new_name = new_base_name + extension

    return new_name