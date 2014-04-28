import requests

from .version import __version__


def _prepare_headers():
    user_agent = "pyweed/{version}".format(version=__version__)
    headers = {"User-Agent": user_agent}
    return headers


def _get_data(url, *args, **kwargs):
    res = requests.get(url, headers=_prepare_headers())
    if res.status_code == 200:
        return res.text
    else:
        return None


def _get_raw_data(url, *args, **kwargs):
    res = requests.get(url, headers=_prepare_headers())
    if res.status_code == 200:
        return res.content
    else:
        return None


def _post_file(url, filename, file_stream):
    res = requests.post(url, files={filename: file_stream},
                        headers=_prepare_headers())
    if res.status_code == 200 or res.status_code == 201:
        return res.text
    else:
        return None


def _delete_data(url, *args, **kwargs):
    res = requests.delete(url)
    if res.status_code == 200 or res.status_code == 202:
        return True
    else:
        return False
