#!/usr/bin/python3
"""This module defines the class FileStorage"""

import json
from models.base_model import BaseModel


class FileStorage:
    """This class serializes instances to a JSON file and deserializes JSON
        file to instances"""

    __file_path = "file.json"  # path to the JSON file
    __objects = {}  # dictionary that stores all objects by <class name>.id

    def all(self):
        """Returns the dictionary __objects"""
        return self.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id"""
        key = obj.__class__.__name__ + "." + obj.id
        self.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)"""
        new_dict = {}
        for key, value in self.__objects.items():
            new_dict[key] = value.to_dict()
        with open(self.__file_path, "w") as f:
            json.dump(new_dict, f)

    def reload(self):
        """Deserializes the JSON file to __objects (only if the JSON file
            (__file_path) exists ; otherwise, do nothing. If the file doesn’t
            exist, no exception should be raised)"""
        try:
            with open(self.__file_path, "r") as f:
                new_dict = json.load(f)
            for key, value in new_dict.items():
                self.__objects[key] = BaseModel(**value)
        except FileNotFoundError:
            pass