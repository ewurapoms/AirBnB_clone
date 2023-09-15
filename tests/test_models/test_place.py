#!/usr/bin/python3
"""Unittests for City Module """

import os
import unittest
from models import storage
from datetime import datetime
from models.place import Place
from models.engine.file_storage import FileStorage


class TestPlace(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self) -> None:
        FileStorage._FileStorage__objects = {}
        if os.path.exists(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_places(self):
        p = Place()
        p1 = Place("welcome", "wait", "enter")
        key = f"{type(p).__name__}.{p.id}"
        self.assertIsInstance(p.name, str)
        self.assertIn(key, storage.all())
        self.assertEqual(p1.name, "")

        self.assertIsInstance(p.name, str)
        self.assertIsInstance(p.user_id, str)
        self.assertIsInstance(p.city_id, str)
        self.assertIsInstance(p.description, str)
        self.assertIsInstance(p.number_bathrooms, int)
        self.assertIsInstance(p.number_rooms, int)
        self.assertIsInstance(p.price_by_night, int)
        self.assertIsInstance(p.max_guest, int)
        self.assertIsInstance(p.longitude, float)
        self.assertIsInstance(p.latitude, float)
        self.assertIsInstance(p.amenity_ids, list)

    def test_init(self):
        p1 = Place()
        p2 = Place(**p1.to_dict())
        self.assertIsInstance(p1.id, str)
        self.assertIsInstance(p1.created_at, datetime)
        self.assertIsInstance(p1.updated_at, datetime)
        self.assertEqual(p1.updated_at, p2.updated_at)

    def test_str(self):
        p1 = Place()
        string = f"[{type(p1).__name__}] ({p1.id}) {p1.__dict__}"
        self.assertEqual(p1.__str__(), string)

    def test_save(self):
        p1 = Place()
        prev = p1.updated_at
        p1.save()
        self.assertNotEqual(p1.updated_at, prev)

    def test_dictionary(self):
        p1 = Place()
        p2 = Place(**p1.to_dict())
        _dict = p2.to_dict()
        self.assertIsInstance(_dict, dict)
        self.assertEqual(_dict['__class__'], type(p2).__name__)
        self.assertIn('created_at', _dict.keys())
        self.assertIn('updated_at', _dict.keys())
        self.assertNotEqual(p1, p2)


if __name__ == "__main__":
    unittest.main()
