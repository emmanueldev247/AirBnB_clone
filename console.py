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


class HBNBCommand(cmd.Cmd):
    """Console class"""
    prompt = "(hbnb) "
    __model_classes = ["BaseModel", "User", "State",
                       "City", "Place", "Amenity", "Review"]

    def do_quit(self, line):
        """quit command exits the console"""
        return True

    def do_EOF(self, line):
        """Ctrl + D exits the console"""
        return True

    def emptyline(self):
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
                print(class_object().id)
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

        all_list = []
        for val in storage.all().values():
            all_list.append(val.__str__())
        print(all_list)

    def do_update(self, line):
        """Updates an instance based on the class name and id Ex:
       (hbnb) update <class name> <id> <attribute name> "<attribute value>" """
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
        attr_value = args[3]

        # Check for the type of attr_value
        try:
            attr_value = int(attr_value)
        except ValueError:
            try:
                attr_value = float(attr_value)
            except ValueError:
                attr_value = str(attr_value).strip("\"")

        setattr(storage_objects[key], attr_name, attr_value)
        storage.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
