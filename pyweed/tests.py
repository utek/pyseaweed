import unittest

import weed


class MiscTests(unittest.TestCase):

    def setUp(self):
        pass

    def test_boundary(self):
        bound = weed._generate_boundary()
        self.assertIsNotNone(bound)
