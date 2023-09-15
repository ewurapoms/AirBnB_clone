#!/usr/bin/python3
"""Unittests for module: State"""

import os
import unittest
from models import storage
from datetime import datetime
from models.state import State
from models.engine.file_storage import FileStorage


class TestState(unittest.TestCase):

    def boot(self):
        pass

    def restart(self) -> None:
        FileStorage._FileStorage__objects = {}
        if os.path.exists(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_parameters(self):
        s = State()
        st = State("hello", "wait", "in")

        key = f"{type(s).__name__}.{s.id}"
        self.assertIsInstance(s.name, str)
        self.assertEqual(st.name, "")
        s.name = "Accra"
        self.assertEqual(s.name, "Accra")
        self.assertIn(key, storage.all())

    def test_init(self):
        st = State()
        st1 = State(**st.to_dict())
        self.assertIsInstance(st.id, str)
        self.assertIsInstance(st.created_at, datetime)
        self.assertIsInstance(st.updated_at, datetime)
        self.assertEqual(st.updated_at, st1.updated_at)

    def test_str(self):
        st = State()
        string = f"[{type(st).__name__}] ({st.id}) {st.__dict__}"
        self.assertEqual(st.__str__(), string)

    def test_save(self):
        st = State()
        prev = st.updated_at
        st.save()
        self.assertNotEqual(st.updated_at, prev)

    def test_dictionary(self):
        st = State()
        st1 = State(**st.to_dict())
        _dict = st1.to_dict()
        self.assertIsInstance(_dict, dict)
        self.assertEqual(_dict['__class__'], type(st1).__name__)
        self.assertIn('created_at', _dict.keys())
        self.assertIn('updated_at', _dict.keys())
        self.assertNotEqual(st, st1)


if __name__ == "__main__":
    unittest.main()
