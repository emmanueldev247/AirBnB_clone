#!/usr/bin/python3
"""defines a City class"""
from models.base_model import BaseModel


class City(BaseModel):
    """represents a city"""
    state_id = ""
    name = ""
