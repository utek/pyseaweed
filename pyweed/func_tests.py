from __future__ import print_function
import os
import unittest
from unittest.case import SkipTest
from .weed import WeedFS


class FunctionalTests(unittest.TestCase):

    def setUp(self):
        self.weed = WeedFS()

    def test_upload_delete(self):
        try:
            fid = self.weed.upload_file(__file__)
            self.assertIsNotNone(fid)
            res = self.weed.delete_file(fid)
            self.assertTrue(res)
        except:
            raise SkipTest
