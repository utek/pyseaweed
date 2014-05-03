# -*- coding: utf-8 -*-
"""This is helper module that contains functions
to easeup communication with weed-fs

.. moduleauthor:: Łukasz Bołdys
"""

import requests

from .version import __version__


def _prepare_headers(additional_headers=None, **kwargs):
    """Prepare headers for http communication.

    Return dict of header to be used in requests.

    Args:
        .. versionadded:: 0.3.2
            **additional_headers**: (optional) Additional headers
            to be used with request

    Returns:
        Headers dict. Key and values are string

    """
    user_agent = "pyweed/{version}".format(version=__version__)
    headers = {"User-Agent": user_agent}
    if additional_headers is not None:
        headers.update(additional_headers)
    return headers


def head(url, *args, **kwargs):
    """Returns response to http HEAD
    on provided url
    """
    res = requests.head(url, headers=_prepare_headers(**kwargs))
    if res.status_code == 200:
        return res
    return None


def get_data(url, *args, **kwargs):
    """Gets data from url as text

    Returns content under the provided url as text

    Args:
        **url**: address of the wanted data

        .. versionadded:: 0.3.2
            **additional_headers**: (optional) Additional headers
            to be used with request

    Returns:
        string

    """
    res = requests.get(url, headers=_prepare_headers(**kwargs))
    if res.status_code == 200:
        return res.text
    else:
        return None


def get_raw_data(url, *args, **kwargs):
    """Gets data from url as bytes

    Returns content under the provided url as bytes
    ie. for binary data

    Args:
        **url**: address of the wanted data

        .. versionadded:: 0.3.2
            **additional_headers**: (optional) Additional headers
            to be used with request

    Returns:
        bytes

    """
    res = requests.get(url, headers=_prepare_headers(**kwargs))
    if res.status_code == 200:
        return res.content
    else:
        return None


def post_file(url, filename, file_stream, *args, **kwargs):
    """Uploads file to provided url.

    Returns contents as text

    Args:
        **url**: address where to upload file

        **filename**: Name of the uploaded file

        **file_stream**: file like object to upload

        .. versionadded:: 0.3.2
            **additional_headers**: (optional) Additional headers
            to be used with request

    Returns:
        string
    """
    res = requests.post(url, files={filename: file_stream},
                        headers=_prepare_headers(**kwargs))
    if res.status_code == 200 or res.status_code == 201:
        return res.text
    else:
        return None


def delete_data(url, *args, **kwargs):
    """Deletes data under provided url

    Returns status as boolean.

    Args:
        **url**: address of file to be deleted

        .. versionadded:: 0.3.2
            **additional_headers**: (optional) Additional headers
            to be used with request

    Returns:
        Boolean. True if request was successful. False if not.
    """
    res = requests.delete(url, headers=_prepare_headers(**kwargs))
    if res.status_code == 200 or res.status_code == 202:
        return True
    else:
        return False
