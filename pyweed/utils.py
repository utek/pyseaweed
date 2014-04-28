import mimetypes
import random
import string
import httplib2
from six.moves import range

from .version import __version__

http = httplib2.Http()


def _get_data(url, *args, **kwargs):
    """helper function"""
    response = None
    user_agent = "pyweed/{version}".format(version=__version__)
    headers = {"User-Agent": user_agent}
    try:
        response, content = http.request(url, headers=headers)
    except Exception as e:
        raise e
    return content.decode("utf-8")


def _get_raw_data(url, *args, **kwargs):
    """helper function"""
    response = None
    user_agent = "pyweed/{version}".format(version=__version__)
    headers = {"User-Agent": user_agent}
    try:
        response, content = http.request(url, headers=headers)
    except Exception as e:
        raise e
    if response.get("status") == "200":
        return content


def _post_data(url, data, *args, **kwargs):
    """helper function"""
    response = None
    user_agent = "pyweed/{version}".format(version=__version__)
    headers = {"User-Agent": user_agent}
    additional_headers = kwargs.get("headers")
    if additional_headers is not None:
        headers.update(additional_headers)
    try:
        response, content = http.request(
            url, "POST", body=data, headers=headers)
    except Exception as e:
        raise e
    return content.decode("utf-8")


def _delete_data(url, *args, **kwargs):
    response = None
    user_agent = "pyweed/{version}".format(version=__version__)
    headers = {"User-Agent": user_agent}
    response, content = http.request(url, "DELETE", headers=headers)
    if response.get("status") == "200" or response.get("status") == "202":
        return True
    else:
        return False


def _generate_boundary():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for x in range(24))


def _file_encode_multipart(filename, file_stream):
    boundary = "weed{0}weed".format(_generate_boundary())
    data = []
    data.append("--{0}".format(boundary))
    data.append('Content-Disposition: form-data; name="file"; filename="{filename}"; type="{file_mimetype}"'.format(
        filename=filename,
        file_mimetype=mimetypes.guess_type(filename)[0] or 'application/octet-stream'))
    data.append("Content-Type: {0}".format(mimetypes.guess_type(
        filename)[0] or 'application/octet-stream'))
    data.append('')
    data.append(file_stream.read())
    data.append('--{0}--'.format(boundary))
    data.append('')
    content_type = 'multipart/form-data; boundary=%s' % boundary
    body = "\n".join(data)
    return content_type, body
