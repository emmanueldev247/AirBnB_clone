#!/usr/bin/python3
"""This module defines the class BaseModel"""

import uuid
from datetime import datetime
import models


class BaseModel:
    """This class defines all common attributes/methods for other classes"""

    def __init__(self, *args, **kwargs):
        """Initializes a new instance of BaseModel"""
        if kwargs:
            # if kwargs is not empty, create an instance from a dictionary
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    # convert string to datetime object
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    # set the attribute with the value
                    setattr(self, key, value)
        else:
            # if kwargs is empty, create a new instance with default values
            self.id = str(uuid.uuid4())  # assign a unique id
            self.created_at = datetime.now()  # assign the current datetime
            self.updated_at = self.created_at  # assign the same datetime as

    def __str__(self):
        """Returns a string representation of the instance"""
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """Updates the public instance attribute updated_at with the current
    datetime"""
        self.updated_at = datetime.now()

    def to_dict(self):
        """Returns a dictionary containing all keys/values of __dict__ of the
            instance"""
        # create a copy of the instance dictionary
        new_dict = self.__dict__.copy()
        # add the class name to the dictionary
        new_dict["__class__"] = self.__class__.__name__
        # convert datetime objects to string in ISO format
        new_dict["created_at"] = self.created_at.isoformat()
        new_dict["updated_at"] = self.updated_at.isoformat()
        # return the new dictionary
        return new_dict
