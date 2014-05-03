from __future__ import print_function
import os
import unittest
from .weed import WeedFS
from .exceptions import BadFidFormat


class FunctionalTests(unittest.TestCase):

    def setUp(self):
        self.weed = WeedFS()

    def test_head_file(self):
        fid = self.weed.upload_file(__file__)
        self.assertIsNotNone(fid)
        res = self.weed.get_file_size(fid)
        self.assertEqual(res, os.path.getsize(__file__))
        res = self.weed.delete_file(fid)
        self.assertTrue(res)
        res = self.weed.get_file_size("3,123456790")
        self.assertIsNone(res)

    def test_upload_delete(self):
        fid = self.weed.upload_file(__file__)
        self.assertIsNotNone(fid)
        res = self.weed.delete_file(fid)
        self.assertTrue(res)

    def test_version(self):
        ver = self.weed.version
        self.assertIsNotNone(ver)

    # Test vacuum generated problems with Weed-FS on windows.
    # TODO: Investigate
    # def test_vacuum(self):
    #     res = self.weed.vacuum()
    #     self.assertTrue(res)

    def test_bad_fid(self):
        self.assertRaises(BadFidFormat, self.weed.get_file_url, ("a"))

    def test_get_file(self):
        fid = self.weed.upload_file(__file__)
        self.assertIsNotNone(fid)
        file_content = self.weed.get_file(fid)
        self.assertIsNotNone(file_content)
        with open(__file__, "rb") as f:
            content = f.read()
        self.assertEqual(content, file_content)
        res = self.weed.delete_file(fid)
        self.assertTrue(res)

    def test_get_wrong_file(self):
        file_content = self.weed.get_file("3,123456790")
        self.assertIsNone(file_content)
