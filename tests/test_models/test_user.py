#!/usr/bin/python3
"""Unittests Model: Class, User"""

import os
import models
import unittest
from time import sleep
from models.user import User
from datetime import datetime


class TestUser_instantiation(unittest.TestCase):

    def test_no_args(self):
        self.assertEqual(User, type(User()))

    def test_objects(self):
        self.assertIn(User(), models.storage.all().values())

    def test_public_id(self):
        self.assertEqual(str, type(User().id))

    def test_public_datetime_created(self):
        self.assertEqual(datetime, type(User().created_at))

    def test_public_datetime_updated(self):
        self.assertEqual(datetime, type(User().updated_at))

    def test_public_email(self):
        self.assertEqual(str, type(User.email))

    def test_public_password(self):
        self.assertEqual(str, type(User.password))

    def test_public_first_name(self):
        self.assertEqual(str, type(User.first_name))

    def test_public_last_name(self):
        self.assertEqual(str, type(User.last_name))

    def test_two_users_unique_ids(self):
        u = User()
        usr = User()
        self.assertNotEqual(u.id, usr.id)

    def test_two_users_different_created_at(self):
        u = User()
        sleep(0.05)
        usr = User()
        self.assertLess(u.created_at, usr.created_at)

    def test_two_users_different_updated_at(self):
        u = User()
        sleep(0.05)
        usr = User()
        self.assertLess(u.updated_at, usr.updated_at)

    def test_str_representation(self):
        u = User()
        u.id = "123456"
        dt = datetime.today()
        dt_rep = repr(dt)
        u.created_at = u.updated_at = dt
        string = u.__str__()
        self.assertIn("[User] (123456)", string)
        self.assertIn("'id': '123456'", string)
        self.assertIn("'created_at': " + dt_rep, string)
        self.assertIn("'updated_at': " + dt_rep, string)

    def test_unused_args(self):
        u = User(None)
        self.assertNotIn(None, u.__dict__.values())

    def test_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        u = User(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(u.id, "345")
        self.assertEqual(u.created_at, dt)
        self.assertEqual(u.updated_at, dt)

    def test_None_kwargs(self):
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)


class TestUser_save(unittest.TestCase):

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_first_save(self):
        u = User()
        sleep(0.05)
        update_one = u.updated_at
        u.save()
        self.assertLess(update_one, u.updated_at)

    def test_double_saves(self):
        u = User()
        sleep(0.05)
        update_one = u.updated_at
        u.save()
        update_two = u.updated_at
        self.assertLess(update_one, update_two)
        sleep(0.05)
        u.save()
        self.assertLess(update_two, u.updated_at)

    def test_save_with_arg(self):
        u = User()
        with self.assertRaises(TypeError):
            u.save(None)

    def test_save_updates(self):
        u = User()
        u.save()
        uid = "User." + u.id
        with open("file.json", "r") as f:
            self.assertIn(uid, f.read())


class TestUser_to_dict(unittest.TestCase):

    def test_to_dict_type(self):
        self.assertTrue(dict, type(User().to_dict()))

    def test_to_dict_keys(self):
        u = User()
        self.assertIn("id", u.to_dict())
        self.assertIn("created_at", u.to_dict())
        self.assertIn("updated_at", u.to_dict())
        self.assertIn("__class__", u.to_dict())

    def test_to_dict_attributes(self):
        u = User()
        u.middle_name = "ALX"
        u.my_number = 98
        self.assertEqual("ALX", u.middle_name)
        self.assertIn("my_number", u.to_dict())

    def test_to_dict_for_str(self):
        u = User()
        u_dict = u.to_dict()
        self.assertEqual(str, type(u_dict["id"]))
        self.assertEqual(str, type(u_dict["created_at"]))
        self.assertEqual(str, type(u_dict["updated_at"]))

    def test_dict_contrast(self):
        u = User()
        self.assertNotEqual(u.to_dict(), u.__dict__)

    def test_dict_with_arg(self):
        u = User()
        with self.assertRaises(TypeError):
            u.to_dict(None)

    def test_final_dict(self):
        u = User()
        u.id = "123456"
        dt = datetime.today()
        u.created_at = u.updated_at = dt
        _dict = {
            'id': '123456',
            '__class__': 'User',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(u.to_dict(), _dict)


if __name__ == "__main__":
    unittest.main()
