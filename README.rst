*********************************************************
PyWeed
*********************************************************

Class to simplify communication with WeedFS


+++++++
Usage
+++++++

Upload file to weedFS

.. code-block:: python

    from pyweed import WeedFS

    w = WeedFS("localhost", 9333) // weed-fs master address and port
    w.upload_file("d:/n.txt") // path to file


.. py:class:: WeedFS
    .. py:method:: __init__(self, master_addr='localhost', master_port=9333)

    .. py:method:: get_file_url(self, fid)
        Get url for the file

        :param integer fid: File ID
        :rtype: str

    .. py:method:: get_file_location(self, volume_id):
        Get location for the file

        :param integer volume_id: volume_id
        :rtype: namedtuple

    .. py:method:: delete_file(self, fid):
        Delete file from WeedFS

        :param string fid: File ID

    .. py:method:: upload_file(self, file_path):
        Uploads file to WeedFS

        :param string file_path:
        :rtype: string or None
