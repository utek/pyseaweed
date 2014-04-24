import unittest

from . import weed


def _mock_request(*args, **kwargs):
    return {"status": "200"}, b"OK"


weed.http.request = _mock_request


class MiscTests(unittest.TestCase):

    def setUp(self):
        pass

    def test_boundary(self):
        bound = weed._generate_boundary()
        self.assertIsNotNone(bound)

    def test_get_data(self):
        content = weed._get_data("url")
        self.assertEqual(content, "OK")

    def test_post_data(self):
        content = weed._post_data("url", "123")
        self.assertEqual(content, "OK")

    def test_delete_data(self):
        content = weed._delete_data("url")
        self.assertTrue(content)
