import exifread

from datetime import datetime

import settings


def get_exif_datetime(file_name):
    img_file = open(str(file_name), 'rb')

    data = exifread.process_file(img_file)

    tag_datetime = data.get('EXIF DateTimeOriginal')

    if tag_datetime:
        parsed_datetime = datetime.strptime(
            str(tag_datetime),
            settings.EXIF_DATETIME_FORMAT
        )

        return parsed_datetime