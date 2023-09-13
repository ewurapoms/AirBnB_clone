#!/usr/bin/python3
"""Defines the FileStorage class."""

import os
import json
import datetime


class FileStorage:
    __file_path = "file.json"
    __objects = {}

    def all(self):
        return FileStorage.__objects

    def new(self, obj):
        key = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        _dict = FileStorage.__objects
        dict_ob = {obj: _dict[obj].to_dict() for obj in _dict.keys()}
        with open(FileStorage.__file_path, "w") as f:
            json.dump(dict_ob, f)

    def reload(self):
        if not os.path.isfile(FileStorage.__file_path):
            return
        with open(FileStorage.__file_path, "r", encoding="utf-8") as f:
            _dict = json.load(f)
            _dict = {key: self.classes()[val["__class__"]](**val)
                     for key, val in _dict.items()}
            FileStorage.__objects = _dict

    def classes(self):
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        classes = {"BaseModel": BaseModel,
                   "User": User,
                   "State": State,
                   "City": City,
                   "Amenity": Amenity,
                   "Place": Place,
                   "Review": Review}
        return classes

    def attributes(self):
        attributes = {
            "BaseModel":
                     {"id": str,
                      "created_at": datetime.datetime,
                      "updated_at": datetime.datetime},
            "User":
                     {"email": str,
                      "password": str,
                      "first_name": str,
                      "last_name": str},
            "State":
                     {"name": str},
            "City":
                     {"state_id": str,
                      "name": str},
            "Amenity":
                     {"name": str},
            "Place":
                     {"city_id": str,
                      "user_id": str,
                      "name": str,
                      "description": str,
                      "main_rooms": int,
                      "bathrooms": int,
                      "guest_count": int,
                      "rate_per_night": int,
                      "latitude": float,
                      "longitude": float,
                      "amenity_data": list},
            "Review":
            {"place_id": str,
                         "user_id": str,
                         "text": str}
        }
        return attributes
