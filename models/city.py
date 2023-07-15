#!/usr/bin/python3
"""This defines the City class."""
from models.base_model import BaseModel


class City(BaseModel):
    """
    City class inherited from BaseModel.

    Public Class Attributes:
        state_id (str): Empty string representing the State ID.
        name (str): Empty string representing name of the city.
    """
    state_id = ""
    name = ""
