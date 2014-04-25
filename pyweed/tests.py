import unittest

from . import utils


def _mock_request(*args, **kwargs):
    return {"status": "200"}, b"OK"


class MiscTests(unittest.TestCase):

    def setUp(self):
        utils.http.request = _mock_request
        pass

    def test_boundary(self):
        bound = utils._generate_boundary()
        self.assertIsNotNone(bound)

    def test_get_data(self):
        content = utils._get_data("url")
        self.assertEqual(content, "OK")

    def test_post_data(self):
        content = utils._post_data("url", "123")
        self.assertEqual(content, "OK")

    def test_delete_data(self):
        content = utils._delete_data("url")
        self.assertTrue(content)
