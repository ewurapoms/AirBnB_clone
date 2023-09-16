#!/usr/bin/python3
"""Defines the command interpreter's entry point"""

import re
import cmd
import json
from models import storage
from models.base_model import BaseModel


class HBNBCommand(cmd.Cmd):

    prompt = "(hbnb) "

    def default(self, arg):
        self.do_cmd(arg)

    def do_cmd(self, arg):
        pair = re.search(r"^(\w*)\.(\w+)(?:\(([^)]*)\))$", line)
        if not pair:
            return arg
        classname = pair.group(1)
        method = pair.group(2)
        args = pair.group(3)
        pair_uid_with_args = re.search('^"([^"]*)"(?:, (.*))?$', args)
        if pair_uid_with_args:
            uid = pair_uid_with_args.group(1)
            attr_or_dict = pair_uid_with_args.group(2)
        else:
            uid = args
            attr_or_dict = False

        attr_and_value = ""
        if method == "update" and attr_or_dict:
            pair_dict = re.search('^({.*})$', attr_or_dict)
            if pair_dict:
                self.update_dict(classname, uid, pair_dict.group(1))
                return ""
            pair_attr_and_value = re.search(
                '^(?:"([^"]*)")?(?:, (.*))?$', attr_or_dict)
            if pair_attr_and_value:
                attr_and_value = (pair_attr_and_value.group(
                    1) or "") + " " + (pair_attr_and_value.group(2) or "")
        command = method + " " + classname + " " + uid + " " + attr_and_value
        self.onecmd(command)
        return command

    def update_dict(self, classname, uid, s_dict):
        """Helper method for update() with a dictionary."""
        serie = s_dict.replace("'", '"')
        deserie = json.loads(serie)
        if not classname:
            print("** class name missing **")
        elif classname not in storage.classes():
            print("** class doesn't exist **")
        elif uid is None:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(classname, uid)
            if key not in storage.all():
                print("** no instance found **")
            else:
                attributes = storage.attributes()[classname]
                for attr, val in deserie.items():
                    if attr in attributes:
                        val = attributes[attribute](val)
                    setattr(storage.all()[key], attr, val)
                storage.all()[key].save()

    def do_EOF(self, arg):
        """Handles End Of File character.
        """
        print()
        return True

    def do_quit(self, arg):
        """Quit command to exit the program
        """
        return True

    def emptyline(self):
        pass

    def do_create(self, arg):
        if arg == "" or arg is None:
            print("** class name missing **")
        elif arg not in storage.classes():
            print("** class doesn't exist **")
        else:
            store = storage.classes()[arg]()
            store.save()
            print(store.id)

    def do_show(self, arg):
        if arg == "" or arg is None:
            print("** class name missing **")
        else:
            words = arg.split(' ')
            if words[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(words) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(words[0], words[1])
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    print(storage.all()[key])

    def do_destroy(self, arg):
        if arg == "" or arg is None:
            print("** class name missing **")
        else:
            comms = arg.split(' ')
            if comms[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(comms) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(comms[0], comms[1])
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    del storage.all()[key]
                    storage.save()

    def do_all(self, arg):
        if arg != "":
            comms = arg.split(' ')
            if comms[0] not in storage.classes():
                print("** class doesn't exist **")
            else:
                tmp = [str(obj) for key, obj in storage.all().items()
                       if type(obj).__name__ == comms[0]]
                print(tmp)
        else:
            new_list = [str(obj) for key, obj in storage.all().items()]
            print(new_list)

    def do_count(self, arg):
        comms = arg.split(' ')
        if not comms[0]:
            print("** class name missing **")
        elif comms[0] not in storage.classes():
            print("** class doesn't exist **")
        else:
            pairs = [
                ele for ele in storage.all() if ele.startswith(
                    comms[0] + '.')]
            print(len(pairs))

    def do_update(self, arg):
        if arg == "" or arg is None:
            print("** class name missing **")
            return

        regx = r'^(\S+)(?:\s(\S+)(?:\s(\S+)(?:\s((?:"[^"]*")|(?:(\S)+)))?)?)?'
        pair = re.search(regx, arg)
        classname = pair.group(1)
        uid = pair.group(2)
        attribute = pair.group(3)
        value = pair.group(4)
        if not pair:
            print("** class name missing **")
        elif classname not in storage.classes():
            print("** class doesn't exist **")
        elif uid is None:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(classname, uid)
            if key not in storage.all():
                print("** no instance found **")
            elif not attribute:
                print("** attribute name missing **")
            elif not value:
                print("** value missing **")
            else:
                cast = None
                if not re.search('^".*"$', value):
                    if '.' in value:
                        cast = float
                    else:
                        cast = int
                else:
                    value = value.replace('"', '')
                attributes = storage.attributes()[classname]
                if attribute in attributes:
                    value = attributes[attribute](value)
                elif cast:
                    try:
                        value = cast(value)
                    except ValueError:
                        pass
                setattr(storage.all()[key], attribute, value)
                storage.all()[key].save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
