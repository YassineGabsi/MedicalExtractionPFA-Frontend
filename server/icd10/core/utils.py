import re


def s3_url_to_bucket_name_keyword(s3_url):
    """
    Transforms s3_url to (bucket_name, keyword) pair.
    :param s3_url: str
    :return: (str, str). (bucket_name, keyword) pair
    """
    match = re.match('s3://([^/]*?)/(.*)', s3_url)
    if match:
        return match.group(1), match.group(2)
    else:
        return None, None


def get_url_type(file_url):
    """
    Returns the type (protocol) of a file url. Protocol can be s3, http, or local (local file).
    :param file_url: str
    :return: str
    """
    if re.match('s3://([^/]*?)/(.*)', file_url):
        return 's3'
    elif re.match('(http|https)://([^/]*?)/(.*)', file_url):
        return 'http'
    else:
        return 'local'


def get_extension(file_url):
    """
    Returns the extension of a file_url.
    :param file_url: str
    :return: str
    """
    if re.match('^.*\\.xls(x|m)?$', file_url):
        return 'excel'
    elif re.match('^.*\\.json$', file_url):
        return 'json'
    elif re.match('^.*\\.xml$', file_url):
        return 'xml'
    elif re.match('^.*\\.csv$', file_url):
        return 'csv'
    else:
        return None


def filepath_or_buffer_to_str(filepath_or_buffer, encoding="utf-8"):
    """
    Transforms filepath_or_buffer to str if filepath_or_buffer is a path or a buffer else returns it.
    :param filepath_or_buffer: Union[str, BytesIO]
    :param encoding: str
    :return: str
    """
    res = None
    try:
        filepath_or_buffer.seek(0)
        res = filepath_or_buffer.read().decode(encoding)
        retry = False
    except:
        retry = True

    if (retry):
        try:
            res = open(filepath_or_buffer, "r", encoding=encoding).read()
            retry = False
        except:
            retry = True

    if (retry):
        res = filepath_or_buffer
    return res
