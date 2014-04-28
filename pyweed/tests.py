import unittest
from httmock import HTTMock
from . import utils
from .weed import WeedFS


def _mock_request(*args, **kwargs):
    return {"status": "200"}, b"OK"


def _mock_bad_request(*args, **kwargs):
    return {"status": "400"}, b"ERROR"


def _mock_exception_request(*args, **kwargs):
    raise Exception
    return {"status": "200"}, b"OK"


def response_content(url, request):
    return {'status_code': 200,
            'content': b"OK"}


class ReqTests(unittest.TestCase):

    def setUp(self):
        pass

    def test_post_file(self):
        with HTTMock(response_content):
            r = utils._post_file("http://utek.pl", "tets.py", open(__file__, "rb"))
            self.assertEqual(r.status_code, 200)

    def test_get_data(self):
        with HTTMock(response_content):
            r = utils._get_data("http://utek.pl")
            self.assertEqual(r.content, "OK")

    def test_delete_data(self):
        with HTTMock(response_content):
            r = utils._delete_data("http://localhost")
            self.assertTrue(r)
        pass


class WeedFSTests(unittest.TestCase):

    def setUp(self):
        self.weed = WeedFS()
        pass

    def test_repr(self):
        self.assertEqual(str(self.weed), "<WeedFS localhost:9333>")
