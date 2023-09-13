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
        _dict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        pair = re.search(r"\.", arg)
        if pair is not None:
            argl = [arg[:pair.span()[0]], arg[pair.span()[1]:]]
            pair = re.search(r"\((.*?)\)", argl[1])
            if pair is not None:
                command = [argl[1][:pair.span()[0]], pair.group()[1:-1]]
                if command[0] in _dict.keys():
                    call = "{} {}".format(argl[0], command[1])
                    return _dict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def update_dict(self, classname, uid, temp):
        """created method for the update()"""
        serie = temp.replace("'", '"')
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
        """Handles End Of File"""
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
