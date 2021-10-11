# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4


from __future__ import print_function

import os
import unittest

from pyseaweed.exceptions import BadFidFormat
from pyseaweed.seaweed import SeaweedFS


class FunctionalTests(unittest.TestCase):
    def setUp(self):
        self.seaweed = SeaweedFS()

    def test_head_file(self):
        _file = os.path.join(os.path.dirname(__file__), "../tox.ini")
        fid = self.seaweed.upload_file(_file)
        self.assertIsNotNone(fid)
        res = self.seaweed.get_file_size(fid)
        # Size is same or lower than file on disk
        self.assertTrue(res <= os.path.getsize(_file))
        res = self.seaweed.delete_file(fid)
        self.assertTrue(res)
        res = self.seaweed.get_file_size("3,123456790")
        self.assertIsNone(res)

    def test_upload_delete(self):
        fid = self.seaweed.upload_file(__file__)
        self.assertIsNotNone(fid)
        res = self.seaweed.delete_file(fid)
        self.assertTrue(res)

    def test_version(self):
        ver = self.seaweed.version
        self.assertIsNotNone(ver)

    def test_exists(self):
        fid = self.seaweed.upload_file(__file__)
        self.assertTrue(self.seaweed.file_exists(fid))
        res = self.seaweed.delete_file(fid)
        self.assertTrue(res)
        self.assertFalse(self.seaweed.file_exists(fid))

    def test_upload_stream(self):
        with open(__file__, "rb") as stream:
            fid = self.seaweed.upload_file(stream=stream, name="test.py")
            self.assertIsNotNone(fid)
        res = self.seaweed.delete_file(fid)
        self.assertTrue(res)

    # Test vacuum generated problems with Weed-FS on windows.
    # TODO: Investigate
    # def test_vacuum(self):
    #     res = self.seaweed.vacuum()
    #     self.assertTrue(res)
    def test_bad_fid(self):
        self.assertRaises(BadFidFormat, self.seaweed.get_file_url, ("a"))

    def test_get_file(self):
        fid = self.seaweed.upload_file(__file__)
        self.assertIsNotNone(fid)
        file_content = self.seaweed.get_file(fid)
        self.assertIsNotNone(file_content)
        with open(__file__, "rb") as f:
            content = f.read()
        self.assertEqual(content, file_content)
        res = self.seaweed.delete_file(fid)
        self.assertTrue(res)

    def test_get_wrong_file(self):
        file_content = self.seaweed.get_file("3,123456790")
        self.assertIsNone(file_content)


class FunctionalTestsSession(unittest.TestCase):
    def setUp(self):
        self.seaweed = SeaweedFS(use_session=True)

    def test_head_file(self):
        _file = os.path.join(os.path.dirname(__file__), "../tox.ini")
        fid = self.seaweed.upload_file(_file)
        self.assertIsNotNone(fid)
        res = self.seaweed.get_file_size(fid)
        # Size is same or lower than file on disk
        self.assertTrue(res <= os.path.getsize(_file))
        res = self.seaweed.delete_file(fid)
        self.assertTrue(res)
        res = self.seaweed.get_file_size("3,123456790")
        self.assertIsNone(res)

    def test_upload_delete(self):
        fid = self.seaweed.upload_file(__file__)
        self.assertIsNotNone(fid)
        res = self.seaweed.delete_file(fid)
        self.assertTrue(res)

    def test_version(self):
        ver = self.seaweed.version
        self.assertIsNotNone(ver)

    def test_exists(self):
        fid = self.seaweed.upload_file(__file__)
        self.assertTrue(self.seaweed.file_exists(fid))
        res = self.seaweed.delete_file(fid)
        self.assertTrue(res)
        self.assertFalse(self.seaweed.file_exists(fid))

    def test_upload_stream(self):
        with open(__file__, "rb") as stream:
            fid = self.seaweed.upload_file(stream=stream, name="test.py")
            self.assertIsNotNone(fid)
        res = self.seaweed.delete_file(fid)
        self.assertTrue(res)

    # Test vacuum generated problems with Weed-FS on windows.
    # TODO: Investigate
    # def test_vacuum(self):
    #     res = self.seaweed.vacuum()
    #     self.assertTrue(res)
    def test_bad_fid(self):
        self.assertRaises(BadFidFormat, self.seaweed.get_file_url, ("a"))

    def test_get_file(self):
        fid = self.seaweed.upload_file(__file__)
        self.assertIsNotNone(fid)
        file_content = self.seaweed.get_file(fid)
        self.assertIsNotNone(file_content)
        with open(__file__, "rb") as f:
            content = f.read()
        self.assertEqual(content, file_content)
        res = self.seaweed.delete_file(fid)
        self.assertTrue(res)

    def test_get_wrong_file(self):
        file_content = self.seaweed.get_file("3,123456790")
        self.assertIsNone(file_content)
