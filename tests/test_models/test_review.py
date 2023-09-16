#!/usr/bin/python3
"""Unittest Module: Review"""

import unittest
from models.review import Review
from models.base_model import BaseModel


class TestReview(unittest.TestCase):

    def setUp(self):
        pass

    def test_instance(self):
        r = Review()
        self.assertEqual(str(type(r)), "<class 'models.review.Review'>")
        self.assertIsInstance(r, Review)
        self.assertTrue(issubclass(Review, BaseModel))

    def test_class_attr(self):
        r = Review()
        self.assertTrue(hasattr(Review, "place_id"))
        self.assertTrue(hasattr(Review, "user_id"))
        self.assertTrue(hasattr(Review, "text"))

    def test_attr_type(self):
        r = Review()
        self.assertTrue(r.place_id == "")
        self.assertTrue(r.user_id == "")
        self.assertTrue(r.text == "")


if __name__ == '__main__':

    unittest.main()
