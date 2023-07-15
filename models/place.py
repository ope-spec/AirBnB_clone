#!/usr/bin/python3
"""This defines the Place class."""

from models.base_model import BaseModel


class Place(BaseModel):
    """
    Place class inherited from BaseModel.

    Public Class Attributes:
        city_id (str): An empty string indicating the associated City ID.
        user_id (str): Empty string indicating the associated User ID.
        name (str): Empty string indicating the place name.
        description (str): Empty string indicating the place description.
        number_rooms (int): Integer value indicating the number
                            of rooms in the place.
        number_bathrooms (int): Integer value indicating the number
                                of bathrooms in the place.
        max_guest (int): Integer value indicating the maximum number
                         of guests allowed in the place.
        price_by_night (int): Integer value indicating the
                              price per night for the place.
        latitude (float): Float value indicating the latitude
                          coordinate of the place.
        longitude (float): Float value indicating the
                           longitude coordinate of the place.
        amenity_ids (list): List of strings indicating the
                            associated Amenity IDs.
    """
    city_id = ""
    user_id = ""
    name = ""
    description = ""
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []
