***************
Intro
***************

Python module to communicate with Seaweed-FS_.


============
Installation
============

From PyPI::

    pip install pyseaweed


From GitHub::

    pip install git+https://github.com/utek/pyseaweed.git


From source::

    git clone git@github.com:utek/pyseaweed.git
    cd pyseaweed
    python setup.py install

============
Tests
============

Install dependencies::

    pip install -r test_requirements.txt

Run tests::

    python setup.py tests

Or using nose::

    nosetests

.. note::
    Functional tests assumes that there is WeedFS master running on localhost:9333 (defaults).
    If it's not then there will be errors in tests.

============
Usage
============

Upload file to weedFS

.. code-block:: python

    from pyseaweed import WeedFS

    # File upload
    w = WeedFS("localhost", 9333) # weed-fs master address and port
    fid = w.upload_file("n.txt") # path to file

    # Get file url
    file_url = w.get_file_url(fid)

    # Delete file
    res = w.delete_file(fid)
    # res is boolean (True if file was deleted)



.. _Weed-FS: https://github.com/chrislusf/seaweedfs
