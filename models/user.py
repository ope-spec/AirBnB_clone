#!/usr/bin/python3
"""
Module: user
Defines the User class.
"""

from models.base_model import BaseModel


class User(BaseModel):
    """
    User class.
    Inherits from BaseModel.
    Represents a user in the system.
    """

    email = ""
    password = ""
    first_name = ""
    last_name = ""

    def __init__(self, *args, **kwargs):
        """
        Initializes a new User instance.
        """
        super().__init__(*args, **kwargs)
