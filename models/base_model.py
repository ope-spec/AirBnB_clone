#!/usr/bin/python3
"""
Module: base_model
Defines the BaseModel class.
"""

import uuid
from datetime import datetime


class BaseModel:
    """
    BaseModel class.
    Defines common attributes/methods for other classes.
    """

    def __init__(self):
        """
        Initializes a new instance of the BaseModel class.

        Attributes:
            id (str): Unique identifier assigned to the instance.
            created_at (datetime): Date and time when the instance is created.
            updated_at (datetime): Date and time when the instance
                                   is last updated.
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at

    def __str__(self):
        """
        Returns a string representation of the BaseModel instance.

        Returns:
            str: String representation in the format:
                 "[<class name>] (<self.id>) <self.__dict__>"
        """
        return "[{}] ({}) {}".format(
            self.__class__.__name__,
            self.id,
            self.__dict__
        )

    def save(self):
        """
        Updates the public instance attribute
        updated_at with the current datetime.
        """
        self.updated_at = datetime.now()

    def to_dict(self):
        """
        Returns a dictionary representation of the BaseModel instance.

        Returns:
            dict: Dictionary containing all keys/values
                  of __dict__ of the instance.
                  Includes the __class__ key with the class name.
                  The created_at and updated_at attributes are
                  converted to string objects in ISO format.
        """
        obj_dict = self.__dict__.copy()
        obj_dict['__class__'] = self.__class__.__name__
        obj_dict['created_at'] = self.created_at.isoformat()
        obj_dict['updated_at'] = self.updated_at.isoformat()
        return obj_dict
