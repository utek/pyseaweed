# -*- coding: utf-8 -*-
__version__ = "0.0.1"


import json
import random
from collections import namedtuple

import httplib2

http = httplib2.Http()


def get_data(url, *args, **kwargs):
    """helper function"""
    response = None
    user_agent = "pyweed/{version}".format(version=__version__)
    headers = {"User-Agent": user_agent}
    try:
        response, content = http.request(url, headers=headers)
    except Exception as e:
        print e
    return content.decode("utf-8")


class WeedFS(object):
    master_addr = "localhost"
    master_port = 9333

    def __init__(self, master_addr='localhost', master_port=9333):
        self.master_addr = master_addr
        self.master_port = master_port

    def get_file_url(self, fid):
        """
        Get url for the file

        :param integer fid: File ID
        :rtype: string
        """
        volume_id, rest = fid.strip().split(",")
        file_location = get_file_location(volume_id)
        url = "http://{public_url}/{fid}".format(file_location.public_url, fid)
        return url

    def get_file_location(self, volume_id):
        """
        Get location for the file

        :param integer volume_id: volume_id
        :rtype: namedtuple
        """
        url = "http://{master_addr}:{master_port}/dir/lookup?volumeId={volume_id}".format(
            master_addr=self.master_addr,
            master_port=self.master_port,
            volume_id=volume_id)
        data = json.loads(get_data(url))
        _file_location = random.choice(data['locations'])
        FileLocation = namedtuple('FileLocation', "public_url url")
        return FileLocation(file_location['publicUrl'], file_location['url'])
