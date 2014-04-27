.. image:: https://travis-ci.org/utek/pyweed.svg?branch=master

*********************************************************
PyWeed
*********************************************************

Class to simplify communication with WeedFS

============
Installation
============

From PyPI

    `pip install pyweed`


============
Usage
============

Upload file to weedFS

.. code-block:: python

    from pyweed import WeedFS

    # File upload
    w = WeedFS("localhost", 9333) # weed-fs master address and port
    fid = w.upload_file("n.txt") # path to file

    # Get file url
    file_url = w.get_file_url(fid)

    # Delete file
    res = w.delete_file(fid)
    # res is boolean (True if file was deleted)




