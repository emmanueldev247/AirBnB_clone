#!/usr/bin/python3
"""User class"""
from models.base_model import BaseModel


class User(BaseModel):
    """stores data of User"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""
