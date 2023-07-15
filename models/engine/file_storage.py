#!/usr/bin/python3
"""
Module: file_storage
Defines the FileStorage class.
"""

import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """
    FileStorage class.
    Serializes instances to a JSON file and
    deserializes JSON file to instances.
    """

    __file_path = "file.json"
    __objects = {}
    classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
    }

    def all(self):
        """
        Returns the dictionary __objects.

        Returns:
            dict: Dictionary containing all objects by <class name>.id.
        """
        return FileStorage.__objects

    def new(self, obj):
        """
        Sets in __objects the given object with key <obj class name>.id.

        Args:
            obj: Instance object to set in __objects.
        """
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """
        Serializes __objects to the JSON file (__file_path).
        """
        obj_dict = {}
        for key, value in FileStorage.__objects.items():
            obj_dict[key] = value.to_dict()
        with open(FileStorage.__file_path, 'w', encoding='utf-8') as file:
            json.dump(obj_dict, file)

    def reload(self):
        """
        Deserializes the JSON file (__file_path) to __objects.
        Only if the JSON file exists; otherwise, do nothing.
        If the file doesn't exist, no exception should be raised.
        """
        try:
            with open(FileStorage.__file_path, 'r', encoding='utf-8') as file:
                obj_dict = json.load(file)
                for key, value in obj_dict.items():
                    class_name, obj_id = key.split('.')
                    cls = self.classes[class_name]
                    obj = cls(**value)
                    self.new(obj)
        except FileNotFoundError:
            pass
