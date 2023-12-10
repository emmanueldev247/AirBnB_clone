#!/usr/bin/python3
"""Entry point of the command interpreter"""


import cmd
import models
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
import re
from shlex import split


class HBNBCommand(cmd.Cmd):
    """Console class"""
    prompt = "(hbnb) "
    __model_classes = ["BaseModel", "User", "State",
                       "City", "Place", "Amenity", "Review"]

    def do_quit(self, line):
        """Quit command to exit the console"""
        return True

    def do_EOF(self, line):
        """Ctrl-D to exit the console"""
        return True

    def emptyline(self):
        """an empty line + ENTER shouldn't execute anything"""
        pass

    def do_create(self, line):
        """Creates a new instance of BaseModel, saves it and prints the id. Ex:
        (hbnb) create <class name>"""

        # split the command line argument
        args = line.split()
        if len(args) == 0:
            print("** class name missing **")
        else:
            class_name = args[0]
            if class_name not in self.__model_classes:
                print("** class doesn't exist **")
            else:
                # getting the class from globals
                class_object = globals()[class_name]
                new_instance = class_object()
                print(new_instance.id)
                storage.save()

    def do_show(self, line):
        """Prints the string representation of an instance. Ex:
        (hbnb) show <class name> <id>"""
        args = line.split()
        if len(args) == 0:
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name not in self.__model_classes:
            print("** class doesn't exist **")
            return

        if len(args) == 1:
            print("** instance id missing **")
            return

        class_id = args[1]
        # getting the __objects dict from storage
        storage_objects = storage.all()
        for key in storage_objects.keys():
            split_key = key.split('.')  # to check both parts of the key
            if len(split_key) == 2:
                model_name = split_key[0]
                model_id = split_key[1]

                if (model_name == class_name) and (model_id == class_id):
                    print(storage_objects[key])
                    return
        print("** no instance found **")

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id. Ex:
        (hbnb) destroy <class name> <id>"""
        args = line.split()
        if len(args) == 0:
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name not in self.__model_classes:
            print("** class doesn't exist **")
            return

        if len(args) == 1:
            print("** instance id missing **")
            return

        class_id = args[1]
        storage_objects = storage.all()
        for key in storage_objects.keys():
            split_key = key.split('.')
            if len(split_key) == 2:
                model_name = split_key[0]
                model_id = split_key[1]

                if (model_name == class_name) and (model_id == class_id):
                    del (storage_objects[key])
                    storage.save()
                    return
        print("** no instance found **")

    def do_all(self, line):
        """Prints all string representation of all instances. Ex:
        (hbnb) all <class name>
or      (hbnb) all"""
        args = line.split()
        if len(args) != 0:
            class_name = args[0]
            if class_name not in self.__model_classes:
                print("** class doesn't exist **")
                return
            else:
                all_list = []
            for instance_id, instance in storage.all().items():
                if instance.__class__.__name__ == class_name:
                    all_list.append(instance.__str__())

        else:
            all_list = []
            for val in storage.all().values():
                all_list.append(val.__str__())

        print(all_list)
        return

    def do_update(self, line):
        """Updates an instance based on the class name and id Ex:
       (hbnb) update <class name> <id> <attribute name> "<attribute value>" """

        if has_curly_braces(line):
            custom_split(line)
            return

        args = line.split()
        if len(args) == 0:
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name not in self.__model_classes:
            print("** class doesn't exist **")
            return

        if len(args) == 1:
            print("** instance id missing **")
            return

        class_id = args[1]
        if class_id.startswith('"'):
            class_id = re.search(r'"([^"]+)"', class_id).group(1)
        elif class_id.startswith("'"):
            class_id = re.search(r'\'([^\']+)\'', class_id).group(1)
        class_id = class_id.rstrip(',')

        seen = False
        storage_objects = storage.all()
        for key in storage_objects.keys():
            split_key = key.split('.')
            if len(split_key) == 2:
                model_name = split_key[0]
                model_id = split_key[1]

                if (model_name == class_name) and (model_id == class_id):
                    seen = True
                    break
        if not seen:
            print("** no instance found **")
            return

        if len(args) == 2:
            print("** attribute name missing **")
            return

        if len(args) == 3:
            print("** value missing **")
            return

        attr_name = args[2]
        if attr_name.startswith('"') and attr_name.endswith(','):
            attr_name = attr_name[1:-2]
        elif attr_name.startswith("'") and attr_name.endswith(","):
            attr_name = attr_name[1:-2]
        if attr_name.startswith('"') and attr_name.endswith('"'):
            attr_name = attr_name[1:-1]
        elif attr_name.startswith("'") and attr_name.endswith("'"):
            attr_name = attr_name[1:-1]
        if attr_name.endswith(","):
            attr_name = attr_name[:-1]

        attr_value = args[3]

        try:
            attr_value = int(attr_value)
        except ValueError:
            try:
                attr_value = float(attr_value)
            except ValueError:
                attr_value = str(attr_value).strip('"\'')

        setattr(storage_objects[key], attr_name, attr_value)
        storage.save()

    def do_count(self, line):
        """Retrieves the number of instances of a class. Ex:
        (hbnb) count <class name>"""
        args = line.split()
        if len(args) == 0:
            return

        class_name = args[0]
        fmt = f"{class_name}."
        _count = sum(1 for key in storage.all() if key.startswith(fmt))
        print(_count)

    def default(self, line):
        """Default behaviour if no command found"""
        arg_dict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", line)
        if match is not None:
            argList = [line[:match.span()[0]], line[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argList[1])
            if match is not None:
                command = [argList[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in arg_dict.keys():
                    call = "{} {}".format(argList[0], command[1])
                    return arg_dict[command[0]](call)
        print("*** Unknown syntax: {}".format(line))
        return False


def has_curly_braces(input_string):
    curly_braces_pattern = r'{.*}'
    return bool(re.search(curly_braces_pattern, input_string))


def custom_split(input_string):
    model_classes = ["BaseModel", "User", "State",
                     "City", "Place", "Amenity", "Review"]
    pattern = r'(\w+)\s+("[^"]+"|[^\s,]+)\s*,?\s*({.*?})?\s*\)?$'
    match = re.match(pattern, input_string)

    if not match:
        print(match)
        return None
    else:
        class_name = match.group(1)
        class_id = match.group(2)
        dict_repr = match.group(3)

        if class_name not in model_classes:
            print("** class doesn't exist **")
            return

        if class_id.startswith('"'):
            class_id = re.search(r'"([^"]+)"', class_id).group(1)
        elif class_id.startswith("'"):
            class_id = re.search(r'\'([^\']+)\'', class_id).group(1)

        seen = False
        storage_objects = storage.all()
        for key in storage_objects.keys():
            split_key = key.split('.')
            if len(split_key) == 2:
                model_name = split_key[0]
                model_id = split_key[1]

                if (model_name == class_name) and (model_id == class_id):
                    seen = True
                    break
        if not seen:
            print("** no instance found **")
            return

        try:
            attr_dict = eval(dict_repr)  # Safely evaluate the dictionary
            if not isinstance(attr_dict, dict):
                raise ValueError
        except (SyntaxError, ValueError):
            print("** Invalid dictionary representation **")
            return

        for attr_name, attr_value in attr_dict.items():
            setattr(storage_objects[key], attr_name, attr_value)
        storage.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
