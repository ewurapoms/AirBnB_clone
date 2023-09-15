#!/usr/bin/python3
"""Unittests Module :City"""

import os
import unittest
from models import storage
from models.city import City
from datetime import datetime
from models.engine.file_storage import FileStorage

c1 = City()
c2 = City(**c1.to_dict())
c3 = City("welcome", "wait", "enter")


class TestCity(unittest.TestCase):

    def setUp(self):
        pass

    def restart(self) -> None:
        FileStorage._FileStorage__objects = {}
        if os.path.exists(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_parameter(self):
        key = f"{type(c1).__name__}.{c1.id}"
        self.assertIsInstance(c1.name, str)
        self.assertEqual(c3.name, "")
        c1.name = "Spintex"
        self.assertEqual(c1.name, "Spintex")

    def test_init(self):
        self.assertIsInstance(c1.id, str)
        self.assertIsInstance(c1.created_at, datetime)
        self.assertIsInstance(c1.updated_at, datetime)
        self.assertEqual(c1.updated_at, c2.updated_at)

    def test_dictionary(self):
        _dict = c2.to_dict()
        self.assertIsInstance(_dict, dict)
        self.assertEqual(_dict['__class__'], type(c2).__name__)
        self.assertIn('created_at', _dict.keys())
        self.assertIn('updated_at', _dict.keys())
        self.assertNotEqual(c1, c2)

    def test_save(self):
        prev = c1.updated_at
        c1.save()
        self.assertNotEqual(c1.updated_at, prev)


if __name__ == "__main__":
    unittest.main()
