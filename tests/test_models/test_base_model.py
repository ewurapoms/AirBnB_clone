#!/usr/bin/python3
"""Unittest module for class: BaseModel"""

import os
import re
import json
import uuid
import time
import unittest
from models import storage
from datetime import datetime
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class TestBaseModel(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        self.resetStorage()
        pass

    def resetStorage(self):
        FileStorage._FileStorage__objects = {}
        if os.path.isfile(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_instantiation(self):
        b = BaseModel()
        self.assertEqual(str(type(b)), "<class 'models.base_model.BaseModel'>")
        self.assertIsInstance(b, BaseModel)
        self.assertTrue(issubclass(type(b), BaseModel))

    def test_init_plenty_args(self):
        self.resetStorage()
        args = [num for num in range(1000)]
        b = BaseModel(0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
        b = BaseModel(*args)

    def test_init_no_args(self):
        self.resetStorage()
        with self.assertRaises(TypeError) as err:
            BaseModel.__init__()
        msg = "__init__() missing 1 required positional argument: 'self'"
        self.assertEqual(str(err.exception), msg)

    def test_attributes(self):
        attributes = storage.attributes()["BaseModel"]
        obj = BaseModel()
        for key, val in attributes.items():
            self.assertTrue(hasattr(obj, key))
            self.assertEqual(type(getattr(obj, key, None)), val)

    def test_datetime_created(self):
        startDate = datetime.now()
        b = BaseModel()
        diff = b.updated_at - b.created_at
        self.assertTrue(abs(diff.total_seconds()) < 0.01)
        diff = b.created_at - startDate
        self.assertTrue(abs(diff.total_seconds()) < 0.1)

    def test_id(self):
        new = [BaseModel().id for i in range(1000)]
        self.assertEqual(len(set(new)), len(new))

    def test_save(self):
        b = BaseModel()
        time.sleep(0.5)
        startDate = datetime.now()
        b.save()
        diff = b.updated_at - startDate
        self.assertTrue(abs(diff.total_seconds()) < 0.01)

    def test_str(self):
        b = BaseModel()
        regx = re.compile(r"^\[(.*)\] \((.*)\) (.*)$")
        res = regx.match(str(b))
        self.assertIsNotNone(res)
        self.assertEqual(res.group(1), "BaseModel")
        self.assertEqual(res.group(2), b.id)
        serie = res.group(3)
        serie = re.sub(r"(datetime\.datetime\([^)]*\))", "'\\1'", serie)
        deserie = json.loads(serie.replace("'", '"'))
        d = b.__dict__.copy()
        d["created_at"] = repr(d["created_at"])
        d["updated_at"] = repr(d["updated_at"])
        self.assertEqual(deserie, d)

    def test_to_dict(self):
        b = BaseModel()
        b.name = "AbMat"
        b.age = 30
        d = b.to_dict()
        self.assertEqual(d["id"], b.id)
        self.assertEqual(d["__class__"], type(b).__name__)
        self.assertEqual(d["created_at"], b.created_at.isoformat())
        self.assertEqual(d["updated_at"], b.updated_at.isoformat())
        self.assertEqual(d["name"], b.name)
        self.assertEqual(d["age"], b.age)

    def test_to_dict_excess_args(self):
        self.resetStorage()
        with self.assertRaises(TypeError) as err:
            BaseModel.to_dict(self, 98)
        msg = "to_dict() takes 1 positional argument but 2 were given"
        self.assertEqual(str(err.exception), msg)

    def test_to_dict_no_args(self):
        self.resetStorage()
        with self.assertRaises(TypeError) as err:
            BaseModel.to_dict()
        msg = "to_dict() missing 1 required positional argument: 'self'"
        self.assertEqual(str(err.exception), msg)

    def test_instance(self):
        my_model = BaseModel()
        my_model.name = "AbMat"
        my_model.my_number = 89
        my_model_json = my_model.to_dict()
        my_new_model = BaseModel(**my_model_json)
        self.assertEqual(my_new_model.to_dict(), my_model.to_dict())

    def test_dict_instance(self):
        data = {"__class__": "BaseModel",
                "updated_at":
                datetime(2050, 12, 30, 23, 59, 59, 123456).isoformat(),
                "created_at": datetime.now().isoformat(),
                "id": uuid.uuid4(),
                "var": "foobar",
                "int": 108,
                "float": 3.14}
        i = BaseModel(**data)
        self.assertEqual(i.to_dict(), data)

    def test_save_args(self):
        self.resetStorage()
        b = BaseModel()
        b.save()
        key = "{}.{}".format(type(b).__name__, b.id)
        d = {key: b.to_dict()}
        self.assertTrue(os.path.isfile(FileStorage._FileStorage__file_path))
        with open(FileStorage._FileStorage__file_path,
                  encoding="utf-8") as f:
            self.assertEqual(len(f.read()), len(json.dumps(d)))
            f.seek(0)
            self.assertEqual(json.load(f), d)

    def test_save_excess_args(self):
        self.resetStorage()
        with self.assertRaises(TypeError) as err:
            BaseModel.save(self, 98)
        msg = "save() takes 1 positional argument but 2 were given"
        self.assertEqual(str(err.exception), msg)

    def test_save_no_args(self):
        self.resetStorage()
        with self.assertRaises(TypeError) as err:
            BaseModel.save()
        msg = "save() missing 1 required positional argument: 'self'"
        self.assertEqual(str(err.exception), msg)


if __name__ == '__main__':
    unittest.main()
