import unittest
from httmock import HTTMock
from . import utils
from .weed import WeedFS


def response_content(url, request):
    return {'status_code': 200,
            'content': b"OK"}


class ReqTests(unittest.TestCase):

    def setUp(self):
        pass

    def test_post_file(self):
        with HTTMock(response_content):
            r = utils.post_file("http://utek.pl", "tets.py", open(__file__, "rb"))
            self.assertEqual(r, "OK")

    def test_get_data(self):
        with HTTMock(response_content):
            r = utils.get_data("http://utek.pl")
            self.assertEqual(r, "OK")

    def test_get_raw_data(self):
        with HTTMock(response_content):
            r = utils.get_raw_data("http://utek.pl")
            self.assertEqual(r, b"OK")

    def test_delete_data(self):
        with HTTMock(response_content):
            r = utils.delete_data("http://localhost")
            self.assertTrue(r)
        pass

    def test_prepare_headers(self):
        headers = utils._prepare_headers()
        self.assertIsInstance(headers, dict)
        for k, v in headers.items():
            self.assertIsInstance(k, str)
            self.assertIsInstance(v, str)


class WeedFSTests(unittest.TestCase):

    def setUp(self):
        self.weed = WeedFS()
        pass

    def test_repr(self):
        self.assertEqual(str(self.weed), "<WeedFS localhost:9333>")
