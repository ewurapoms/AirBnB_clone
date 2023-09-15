#!/usr/bin/python3
"""Unittest for class: FileStorage"""

import re
import os
import json
import time
import unittest
from models import storage
from datetime import datetime
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):

    def setUp(self):
        pass

    def resetStorage(self):
        FileStorage._FileStorage__objects = {}
        if os.path.isfile(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def tearDown(self):
        self.resetStorage()
        pass

    def test_5_instantiation(self):
        self.assertEqual(type(storage).__name__, "FileStorage")

    def test_3_init_no_args(self):
        self.resetStorage()
        with self.assertRaises(TypeError) as err:
            FileStorage.__init__()
        msg = "descriptor '__init__' of 'object' object needs an argument"
        self.assertEqual(str(err.exception), msg)

    def test_5_attributes(self):
        self.resetStorage()
        self.assertTrue(hasattr(FileStorage, "_FileStorage__file_path"))
        self.assertTrue(hasattr(FileStorage, "_FileStorage__objects"))
        self.assertEqual(getattr(FileStorage, "_FileStorage__objects"), {})

    def help_test_all(self, classname):
        self.resetStorage()
        self.assertEqual(storage.all(), {})

        o = storage.classes()[classname]()
        storage.new(o)
        key = "{}.{}".format(type(o).__name__, o.id)
        self.assertTrue(key in storage.all())
        self.assertEqual(storage.all()[key], o)

    def test_5_all_base_model(self):
        self.help_test_all("BaseModel")

    def test_5_all_user(self):
        self.help_test_all("User")

    def test_5_all_state(self):
        self.help_test_all("State")

    def test_5_all_city(self):
        self.help_test_all("City")

    def test_5_all_amenity(self):
        self.help_test_all("Amenity")

    def test_5_all_place(self):
        self.help_test_all("Place")

    def test_5_all_review(self):
        self.help_test_all("Review")

    def help_test_all_multiple(self, classname):
        self.resetStorage()
        self.assertEqual(storage.all(), {})

        cls = storage.classes()[classname]
        objs = [cls() for i in range(1000)]
        [storage.new(o) for o in objs]
        self.assertEqual(len(objs), len(storage.all()))
        for o in objs:
            key = "{}.{}".format(type(o).__name__, o.id)
            self.assertTrue(key in storage.all())
            self.assertEqual(storage.all()[key], o)

    def test_5_all_multiple_base_model(self):
        self.help_test_all_multiple("BaseModel")

    def test_5_all_multiple_user(self):
        self.help_test_all_multiple("User")

    def test_5_all_multiple_state(self):
        self.help_test_all_multiple("State")

    def test_5_all_multiple_city(self):
        self.help_test_all_multiple("City")

    def test_5_all_multiple_amenity(self):
        self.help_test_all_multiple("Amenity")

    def test_5_all_multiple_place(self):
        self.help_test_all_multiple("Place")

    def test_5_all_multiple_review(self):
        self.help_test_all_multiple("Review")

    def test_5_all_no_args(self):
        self.resetStorage()
        with self.assertRaises(TypeError) as err:
            FileStorage.all()
        msg = "all() missing 1 required positional argument: 'self'"
        self.assertEqual(str(err.exception), msg)

    def test_5_all_excess_args(self):
        self.resetStorage()
        with self.assertRaises(TypeError) as err:
            FileStorage.all(self, 98)
        msg = "all() takes 1 positional argument but 2 were given"
        self.assertEqual(str(err.exception), msg)

    def help_test_new(self, classname):
        self.resetStorage()
        cls = storage.classes()[classname]
        o = cls()
        storage.new(o)
        key = "{}.{}".format(type(o).__name__, o.id)
        self.assertTrue(key in FileStorage._FileStorage__objects)
        self.assertEqual(FileStorage._FileStorage__objects[key], o)

    def test_5_new_base_model(self):
        self.help_test_new("BaseModel")

    def test_5_new_user(self):
        self.help_test_new("User")

    def test_5_new_state(self):
        self.help_test_new("State")

    def test_5_new_city(self):
        self.help_test_new("City")

    def test_5_new_amenity(self):
        self.help_test_new("Amenity")

    def test_5_new_place(self):
        self.help_test_new("Place")

    def test_new_review_args(self):
        self.help_test_new("Review")

    def test_excess_new_args(self):
        self.resetStorage()
        b = BaseModel()
        with self.assertRaises(TypeError) as err:
            storage.new(b, 98)
        msg = "new() takes 2 positional arguments but 3 were given"
        self.assertEqual(str(err.exception), msg)

    def test_no_new_args(self):
        self.resetStorage()
        with self.assertRaises(TypeError) as err:
            storage.new()
        msg = "new() missing 1 required positional argument: 'obj'"
        self.assertEqual(str(err.exception), msg)

    def help_test_save(self, classname):
        self.resetStorage()
        cls = storage.classes()[classname]
        o = cls()
        storage.new(o)
        key = "{}.{}".format(type(o).__name__, o.id)
        storage.save()
        self.assertTrue(os.path.isfile(FileStorage._FileStorage__file_path))
        d = {key: o.to_dict()}
        with open(FileStorage._FileStorage__file_path,
                  encoding="utf-8") as f:
            self.assertEqual(len(f.read()), len(json.dumps(d)))
            f.seek(0)
            self.assertEqual(json.load(f), d)

    def test_5_save_base_model(self):
        self.help_test_save("BaseModel")

    def test_5_save_user(self):
        self.help_test_save("User")

    def test_5_save_state(self):
        self.help_test_save("State")

    def test_5_save_city(self):
        self.help_test_save("City")

    def test_5_save_amenity(self):
        self.help_test_save("Amenity")

    def test_5_save_place(self):
        self.help_test_save("Place")

    def test_5_save_review(self):
        self.help_test_save("Review")

    def test_5_save_excess_args(self):
        self.resetStorage()
        with self.assertRaises(TypeError) as err:
            FileStorage.save(self, 98)
        msg = "save() takes 1 positional argument but 2 were given"
        self.assertEqual(str(err.exception), msg)

    def test_5_save_no_args(self):
        self.resetStorage()
        with self.assertRaises(TypeError) as err:
            FileStorage.save()
        msg = "save() missing 1 required positional argument: 'self'"
        self.assertEqual(str(err.exception), msg)

    def help_test_reload(self, classname):
        self.resetStorage()
        storage.reload()
        self.assertEqual(FileStorage._FileStorage__objects, {})
        cls = storage.classes()[classname]
        ob = cls()
        storage.new(ob)
        key = "{}.{}".format(type(ob).__name__, ob.id)
        storage.save()
        storage.reload()
        self.assertEqual(ob.to_dict(), storage.all()[key].to_dict())

    def test_5_reload_base_model(self):
        self.help_test_reload("BaseModel")

    def test_5_reload_user(self):
        self.help_test_reload("User")

    def test_5_reload_state(self):
        self.help_test_reload("State")

    def test_5_reload_city(self):
        self.help_test_reload("City")

    def test_5_reload_amenity(self):
        self.help_test_reload("Amenity")

    def test_5_reload_place(self):
        self.help_test_reload("Place")

    def test_5_reload_review(self):
        self.help_test_reload("Review")

    def help_test_reload_mismatch(self, classname):
        self.resetStorage()
        storage.reload()
        self.assertEqual(FileStorage._FileStorage__objects, {})

        cls = storage.classes()[classname]
        o = cls()
        storage.new(o)
        key = "{}.{}".format(type(o).__name__, o.id)
        storage.save()
        o.name = "Poms"
        storage.reload()
        self.assertNotEqual(o.to_dict(), storage.all()[key].to_dict())

    def test_5_reload_mismatch_base_model(self):
        self.help_test_reload_mismatch("BaseModel")

    def test_5_reload_mismatch_user(self):
        self.help_test_reload_mismatch("User")

    def test_5_reload_mismatch_state(self):
        self.help_test_reload_mismatch("State")

    def test_5_reload_mismatch_city(self):
        self.help_test_reload_mismatch("City")

    def test_5_reload_mismatch_amenity(self):
        self.help_test_reload_mismatch("Amenity")

    def test_5_reload_mismatch_place(self):
        self.help_test_reload_mismatch("Place")

    def test_5_reload_mismatch_review(self):
        self.help_test_reload_mismatch("Review")

    def test_5_reload_excess_args(self):
        self.resetStorage()
        with self.assertRaises(TypeError) as err:
            FileStorage.reload(self, 98)
        msg = "reload() takes 1 positional argument but 2 were given"
        self.assertEqual(str(err.exception), msg)

    def test_5_reload_no_args(self):
        self.resetStorage()
        with self.assertRaises(TypeError) as err:
            FileStorage.reload()
        msg = "reload() missing 1 required positional argument: 'self'"
        self.assertEqual(str(err.exception), msg)


if __name__ == '__main__':
    unittest.main()
