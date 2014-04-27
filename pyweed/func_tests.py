from __future__ import print_function
import os
import unittest
from .weed import WeedFS
from .exceptions import BadFidFormat


class FunctionalTests(unittest.TestCase):

    def setUp(self):
        self.weed = WeedFS()

    def test_upload_delete(self):
        fid = self.weed.upload_file(__file__)
        self.assertIsNotNone(fid)
        res = self.weed.delete_file(fid)
        self.assertTrue(res)

    def test_version(self):
        ver = self.weed.version
        self.assertIsNotNone(ver)

    def test_vacuum(self):
        res = self.weed.vacuum()
        self.assertTrue(res)

    def test_bad_fid(self):
        self.assertRaises(BadFidFormat, self.weed.get_file_url, ("a"))

    def test_no_file(self):
        res = self.weed.get_file_url("2,123")
        print(res)
        self.assertIsNone(res)
