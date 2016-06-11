# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4


from __future__ import print_function

import os
import unittest

from pyseaweed.exceptions import BadFidFormat
from pyseaweed.weed import WeedFS


class FunctionalTests(unittest.TestCase):

    def setUp(self):
        self.weed = WeedFS()

    def test_head_file(self):
        _file = os.path.join(os.path.dirname(__file__), "../tox.ini")
        print(_file)
        fid = self.weed.upload_file(_file)
        self.assertIsNotNone(fid)
        res = self.weed.get_file_size(fid)
        self.assertEqual(res, os.path.getsize(_file))
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

    def test_exists(self):
        fid = self.weed.upload_file(__file__)
        self.assertTrue(self.weed.file_exists(fid))
        res = self.weed.delete_file(fid)
        self.assertTrue(res)
        self.assertFalse(self.weed.file_exists(fid))

    def test_upload_stream(self):
        with open(__file__, "rb") as stream:
            fid = self.weed.upload_file(stream=stream, name="test.py")
            self.assertIsNotNone(fid)
        res = self.weed.delete_file(fid)
        self.assertTrue(res)

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


class FunctionalTestsSession(unittest.TestCase):

    def setUp(self):
        self.weed = WeedFS(use_session=True)

    def test_head_file(self):
        _file = os.path.join(os.path.dirname(__file__), "../tox.ini")
        print(_file)
        fid = self.weed.upload_file(_file)
        self.assertIsNotNone(fid)
        res = self.weed.get_file_size(fid)
        self.assertEqual(res, os.path.getsize(_file))
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

    def test_exists(self):
        fid = self.weed.upload_file(__file__)
        self.assertTrue(self.weed.file_exists(fid))
        res = self.weed.delete_file(fid)
        self.assertTrue(res)
        self.assertFalse(self.weed.file_exists(fid))

    def test_upload_stream(self):
        with open(__file__, "rb") as stream:
            fid = self.weed.upload_file(stream=stream, name="test.py")
            self.assertIsNotNone(fid)
        res = self.weed.delete_file(fid)
        self.assertTrue(res)

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
