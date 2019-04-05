import arrow
import os
import mimetypes

additional_file_types = {
    '.md': 'text/markdown',
    '.MOV': 'video/mov'
}


def datetimeformat(date_str):
    dt = arrow.get(date_str).shift(hours=3)
    return dt.humanize(locale='pt_br')

def file_type(key):
    file_info = os.path.splitext(key)
    file_extension = file_info[1]
    try:
        return mimetypes.types_map[file_extension]
    except KeyError:
        filetype = 'Unknown'
        if file_info[0].startswith('.') and file_extension == '':
            filetype = 'text'

        if file_extension in additional_file_types.keys():
            filetype = additional_file_types[file_extension]

        return filetype