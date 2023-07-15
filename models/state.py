#!/usr/bin/python3
"""This defines the State class."""

from models.base_model import BaseModel


class State(BaseModel):
    """
    State class.
    Inherits from BaseModel.
    Public class attributes:
        name: string - empty string representing the name of state.
    """
    name = ""
