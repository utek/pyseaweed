# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4


"""Main PySeaweed module. Contains SeaweedFS class
"""

import json
import os
import random
from collections import namedtuple

from pyseaweed.exceptions import BadFidFormat
from pyseaweed.utils import Connection


class SeaweedFS(object):
    master_addr = "localhost"
    master_port = 9333

    def __init__(
        self,
        master_addr="localhost",
        master_port=9333,
        use_session=False,
        use_public_url=True,
    ):
        """Creates SeaweedFS instance.

        Args:
            **master_addr**: Address of Seaweed-fs master server
                             (default: localhost)

            **master_port**: Weed-fs master server port (default: 9333)
            **use_session**: Use request.Session() for connections instead of
                             requests themselves. (default: False)
            **use_public_url**: If ``True``, all the requests will use
                             ``publicUrl`` link instead of ``url``.

        Returns:
            SeaweedFS instance.
        """
        self.master_addr = master_addr
        self.master_port = master_port
        self.conn = Connection(use_session)
        self.use_public_url = use_public_url

    def __repr__(self):
        return "<{0} {1}:{2}>".format(
            self.__class__.__name__, self.master_addr, self.master_port
        )

    def get_file(self, fid):
        """Get file from SeaweedFS.

        Returns file content. May be problematic for large files as content is
        stored in memory.

        Args:
            **fid**: File identifier <volume_id>,<file_name_hash>

        Returns:
            Content of the file with provided fid or None if file doesn't
            exist on the server

        .. versionadded:: 0.3.1
        """
        url = self.get_file_url(fid)
        return self.conn.get_raw_data(url)

    def get_file_url(self, fid, public=None):
        """
        Get url for the file

        :param string fid: File ID
        :param boolean public: public or internal url
        :rtype: string
        """
        try:
            volume_id, rest = fid.strip().split(",")
        except ValueError:
            raise BadFidFormat(
                "fid must be in format: <volume_id>,<file_name_hash>"
            )
        file_location = self.get_file_location(volume_id)
        if public is None:
            public = self.use_public_url
        volume_url = file_location.public_url if public else file_location.url
        url = "http://{volume_url}/{fid}".format(
            volume_url=volume_url, fid=fid
        )
        return url

    def get_file_location(self, volume_id):
        """
        Get location for the file,
        SeaweedFS volume is choosed randomly

        :param integer volume_id: volume_id
        :rtype: namedtuple `FileLocation` `{"public_url":"", "url":""}`
        """
        url = (
            "http://{master_addr}:{master_port}/"
            "dir/lookup?volumeId={volume_id}"
        ).format(
            master_addr=self.master_addr,
            master_port=self.master_port,
            volume_id=volume_id,
        )
        data = json.loads(self.conn.get_data(url))
        _file_location = random.choice(data["locations"])
        FileLocation = namedtuple("FileLocation", "public_url url")
        return FileLocation(_file_location["publicUrl"], _file_location["url"])

    def get_file_size(self, fid):
        """
        Gets size of uploaded file on SeaweedFS volume. For some type of files
        Gzip Compression might be applied.
        Or None if file doesn't exist.

        Args:
            **fid**: File identifier <volume_id>,<file_name_hash>

        Returns:
            Int or None
        """
        url = self.get_file_url(fid)
        res = self.conn.head(url)
        if res is not None:
            size = res.headers.get("content-length", None)
            if size is not None:
                return int(size)
        return None

    def file_exists(self, fid):
        """Checks if file with provided fid exists

        Args:
            **fid**: File identifier <volume_id>,<file_name_hash>

        Returns:
            True if file exists. False if not.
        """
        res = self.get_file_size(fid)
        if res is not None:
            return True
        return False

    def delete_file(self, fid):
        """
        Delete file from SeaweedFS

        :param string fid: File ID
        """
        url = self.get_file_url(fid)
        return self.conn.delete_data(url)

    def upload_file(self, path=None, stream=None, name=None, **kwargs):
        """
        Uploads file to SeaweedFS

        I takes either path or stream and name and upload it
        to SeaweedFS server.

        Returns fid of the uploaded file.

        :param string path:
        :param string stream:
        :param string name:
        :rtype: string or None

        """
        params = "&".join(["%s=%s" % (k, v) for k, v in kwargs.items()])
        url = "http://{master_addr}:{master_port}/dir/assign{params}".format(
            master_addr=self.master_addr,
            master_port=self.master_port,
            params="?" + params if params else "",
        )
        data = json.loads(self.conn.get_data(url))
        if data.get("error") is not None:
            return None
        post_url = "http://{url}/{fid}".format(
            url=data["publicUrl" if self.use_public_url else "url"],
            fid=data["fid"],
        )

        if path is not None:
            filename = os.path.basename(path)
            with open(path, "rb") as file_stream:
                res = self.conn.post_file(post_url, filename, file_stream)
        # we have file like object and filename
        elif stream is not None and name is not None:
            res = self.conn.post_file(post_url, name, stream)
        else:
            raise ValueError(
                "If `path` is None then *both* `stream` and `name` must not"
                " be None "
            )
        response_data = json.loads(res)
        if "size" in response_data:
            return data.get("fid")
        return None

    def vacuum(self, threshold=0.3):
        """
        Force garbage collection

        :param float threshold (optional): The threshold is optional, and
        will not change the default threshold.
        :rtype: boolean

        """
        url = (
            "http://{master_addr}:{master_port}/"
            "vol/vacuum?garbageThreshold={threshold}"
        ).format(
            master_addr=self.master_addr,
            master_port=self.master_port,
            threshold=threshold,
        )
        res = self.conn.get_data(url)
        if res is not None:
            return True
        return False

    @property
    def version(self):
        """
        Returns Weed-FS master version

        :rtype: string
        """
        url = "http://{master_addr}:{master_port}/dir/status".format(
            master_addr=self.master_addr, master_port=self.master_port
        )
        data = self.conn.get_data(url)
        response_data = json.loads(data)
        return response_data.get("Version")


if __name__ == "__main__":
    pass
