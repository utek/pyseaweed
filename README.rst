*********************************************************
PyWeed
*********************************************************

Class to simplify communication with WeedFS


+++++++
Usage
+++++++

Upload file to weedFS

.. code-block:: python

    w = WeedFS("localhost", 9333) // weed-fs master address and port
    w.upload_file("d:/n.txt") // path to file