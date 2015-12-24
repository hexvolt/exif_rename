import exifread

from datetime import datetime

EXIF_DATETIME_FORMAT = "%Y:%m:%d %H:%M:%S"


def get_exif_datetime(file_name):
    img_file = open(str(file_name), 'rb')

    data = exifread.process_file(img_file)

    tag_datetime = data.get('EXIF DateTimeOriginal')

    if tag_datetime:
        parsed_datetime = datetime.strptime(
            date_string=str(tag_datetime),
            format=EXIF_DATETIME_FORMAT
        )

        return parsed_datetime