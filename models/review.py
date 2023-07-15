#!/usr/bin/python3
"""This defines the Review class."""
from models.base_model import BaseModel

class Review(BaseModel):
    """
    Review class inherited from BaseModel.

    Public Class Attributes:
        place_id (str): Empty string indicating the associated Place ID.
        user_id (str): Empty string indicating the associated User ID.
        text (str): Empty string indicating the review text.
    """
    place_id = ""
    user_id = ""
    text = ""
