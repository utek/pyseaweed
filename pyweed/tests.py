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

    def test_file_encode_multipart(self):
        import os
        with open(__file__, "rb") as file_stream:
            content_type, body = utils._file_encode_multipart(
                os.path.basename(__file__),
                file_stream)
            self.assertIsNotNone(content_type)
            m = content_type.split(";")[0].strip()
            self.assertEqual(m, "multipart/form-data")
