# -*- coding: utf-8 -*-
__version__ = "0.1.0"


import json
import os
import sys
import mimetypes
import random
import string
from collections import namedtuple

import httplib2

http = httplib2.Http()


def _get_data(url, *args, **kwargs):
    """helper function"""
    response = None
    user_agent = "pyweed/{version}".format(version=__version__)
    headers = {"User-Agent": user_agent}
    try:
        response, content = http.request(url, headers=headers)
    except Exception as e:
        print e
    return content.decode("utf-8")


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
        print e
        return "{}"
    return content.decode("utf-8")


def _delete_data(url, *args, **kwargs):
    response = None
    user_agent = "pyweed/{version}".format(version=__version__)
    headers = {"User-Agent": user_agent}
    response, content = http.request(url, "DELETE", headers=headers)
    if response.get("status") == "200":
        return True
    else:
        return False


def _generate_boundary():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for x in xrange(24))


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
    pass


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
        file_location = self.get_file_location(volume_id)
        url = "http://{public_url}/{fid}".format(public_url=file_location.public_url, fid=fid)
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
        data = json.loads(_get_data(url))
        _file_location = random.choice(data['locations'])
        FileLocation = namedtuple('FileLocation', "public_url url")
        return FileLocation(_file_location['publicUrl'], _file_location['url'])

    def delete_file(self, fid):
        """
        Delete file from WeedFS

        :param string fid: File ID
        """
        url = self.get_file_url(fid)
        return _delete_data(url)

    def upload_file(self, file_path):
        '''
        Uploads file to WeedFS

        :param string file_path:
        :rtype: string or None
        '''
        url = "http://{master_addr}:{master_port}/dir/assign".format(
            master_addr=self.master_addr,
            master_port=self.master_port)
        data = json.loads(_get_data(url))
        if data.get("error") is not None:
            print data.get("error")
            return None
        file_stream = open(file_path, "rb")
        filename = os.path.basename(file_path)
        content_type, body = _file_encode_multipart(filename, file_stream)
        post_url = "http://{publicUrl}/{fid}".format(**data)
        file_stream.close()
        res = _post_data(
            post_url, body, headers={"Content-Type": content_type,
                                     "Content-Length": str(len(body)),
                                     "Accept": "*/*"})
        response_data = json.loads(res)
        size = response_data.get('size')
        if size is not None:
            return data['fid']
        else:
            return None


if __name__ == "__main__":
    print "uploading file"
    w = WeedFS("localhost", 9333)
    fid = w.upload_file("d:/n.txt")
    if fid is None:
        sys.exit(0)
    print "fid: {0}".format(fid)

    print "getting link for file: {0}".format(fid)
    url = w.get_file_url(fid)
    print "url: {0}".format(url)
    # deleting
    print "deleting file"
    # res = w.delete_file(fid)
    # print res
