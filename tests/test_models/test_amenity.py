#!/usr/bin/python3
"""Defines Unittest module for class: Amenity"""

import re
import os
import json
import time
import unittest
from models import storage
from datetime import datetime
from models.amenity import Amenity
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class TestAmenity(unittest.TestCase):

    def starter(self):
        pass

    def undo(self):
        self.resetStorage()
        pass

    def resetStorage(self):
        FileStorage._FileStorage__objects = {}
        if os.path.isfile(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_instance(self):
        a = Amenity()
        self.assertEqual(str(type(a)), "<class 'models.amenity.Amenity'>")
        self.assertIsInstance(a, Amenity)
        self.assertTrue(issubclass(type(a), BaseModel))

    def test_attributes(self):
        attributes = storage.attributes()["Amenity"]
        a = Amenity()
        for key, val in attributes.items():
            self.assertTrue(hasattr(a, key))
            self.assertEqual(type(getattr(a, key, None)), val)


if __name__ == "__main__":
    unittest.main()
