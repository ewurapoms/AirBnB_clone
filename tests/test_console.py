#!/usr/bin/python3
"""Defines unittests for console.py"""

import os
import sys
import unittest
from io import StringIO
from models import storage
from models.user import User
from models.city import City
from models.state import State
from models.place import Place
from console import HBNBCommand
from models.review import Review
from models.amenity import Amenity
from models.base_model import BaseModel
from unittest.mock import create_autospec, patch


class TestConsole(unittest.TestCase):

    def setUp(self):
        self.mock_stdin = create_autospec(sys.stdin)
        self.mock_stdout = create_autospec(sys.stdout)
        self.err = ["** class name missing **",
                    "** class doesn't exist **",
                    "** instance id missing **",
                    "** no instance found **",
                    ]

        self.cls = ["BaseModel",
                    "User",
                    "State",
                    "City",
                    "Place",
                    "Amenity",
                    "Review"]

    def create(self, server=None):
        return HBNBCommand(stdin=self.mock_stdin, stdout=self.mock_stdout)

    def finalize(self, x=None):
        if x is None:
            return self.mock_stdout.write.call_args[0][0]
        return "".join(map(lambda c: c[0][0],
                           self.mock_stdout.write.call_args_list[-x:]))

    def test_quit(self):
        cli = self.create()
        self.assertTrue(cli.onecmd("quit"))


if __name__ == '__main__':
    unittest.main()
