# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4


import unittest

from httmock import HTTMock

from pyseaweed.seaweed import SeaweedFS
from pyseaweed.utils import Connection


def response_content(url, request):
    return {"status_code": 200, "content": b"OK"}


def response_content_201(url, request):
    return {"status_code": 201, "content": b"OK"}


def response_content_202(url, request):
    return {"status_code": 202, "content": b"OK"}


def response_content_404(url, request):
    return {"status_code": 404, "content": b"NOK"}


class ReqTests(unittest.TestCase):
    def setUp(self):
        self.conn = Connection()
        pass

    def test_post_file(self):
        with HTTMock(response_content):
            r = self.conn.post_file(
                "http://utek.pl", "tests.py", open(__file__, "rb")
            )
            self.assertEqual(r, "OK")
        with HTTMock(response_content_201):
            r = self.conn.post_file(
                "http://utek.pl", "tests.py", open(__file__, "rb")
            )
            self.assertEqual(r, "OK")
        with HTTMock(response_content_404):
            r = self.conn.post_file(
                "http://utek.pl", "tests.py", open(__file__, "rb")
            )
            self.assertIsNone(r)

    def test_get_data(self):
        with HTTMock(response_content):
            r = self.conn.get_data("http://utek.pl")
            self.assertEqual(r, "OK")
        with HTTMock(response_content_404):
            r = self.conn.get_data("http://utek.pl")
            self.assertIsNone(r)

    def test_get_raw_data(self):
        with HTTMock(response_content):
            r = self.conn.get_raw_data("http://utek.pl")
            self.assertEqual(r, b"OK")
        with HTTMock(response_content_404):
            r = self.conn.get_raw_data("http://utek.pl")
            self.assertIsNone(r)

    def test_delete_data(self):
        with HTTMock(response_content):
            r = self.conn.delete_data("http://localhost")
            self.assertTrue(r)
        with HTTMock(response_content_202):
            r = self.conn.delete_data("http://localhost")
            self.assertTrue(r)
        with HTTMock(response_content_404):
            r = self.conn.delete_data("http://localhost")
            self.assertFalse(r)

    def test_prepare_headers(self):
        headers = self.conn._prepare_headers()
        self.assertIsInstance(headers, dict)
        for k, v in headers.items():
            self.assertIsInstance(k, str)
            self.assertIsInstance(v, str)

    def test_additional_headers(self):
        additional_headers = {"X-Test": "123"}
        kwargs = {"additional_headers": additional_headers}
        headers = self.conn._prepare_headers(**kwargs)
        self.assertIsInstance(headers, dict)
        self.assertIsNotNone(headers.get("X-Test"))
        with HTTMock(response_content):
            r = self.conn.post_file(
                "http://utek.pl",
                "tests.py",
                open(__file__, "rb"),
                additional_headers=additional_headers,
            )
            self.assertEqual(r, "OK")
            r = self.conn.get_data(
                "http://utek.pl", additional_headers=additional_headers
            )
            self.assertEqual(r, "OK")
            r = self.conn.get_raw_data(
                "http://utek.pl", additional_headers=additional_headers
            )
            self.assertEqual(r, b"OK")
            r = self.conn.delete_data(
                "http://localhost", additional_headers=additional_headers
            )
            self.assertTrue(r)


class SeaweedFSTests(unittest.TestCase):
    def setUp(self):
        self.seaweed = SeaweedFS()
        pass

    def test_repr(self):
        self.assertEqual(str(self.seaweed), "<SeaweedFS localhost:9333>")

    def test_exception(self):
        with HTTMock(response_content):
            with self.assertRaises(ValueError):
                self.seaweed.upload_file(stream=None, name="test.py")
            with self.assertRaises(ValueError):
                self.seaweed.upload_file(stream=open(__file__, "rb"))
