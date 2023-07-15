#!/usr/bin/python3
"""This defines the Amenity class."""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """
    Amenity class inherited from BaseModel.

    Public Class Attributes:
        name (str): Empty string representing the name of amenity.
    """
    name = ""
