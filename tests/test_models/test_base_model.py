#!/usr/bin/python3
"""Defines unittests for models/base_model.py.

Unittest classes:
    TestBaseModel_instantiation
    TestBaseModel_save
    TestBaseModel_to_dict
"""

import unittest
from models.base_model import BaseModel
from datetime import datetime
from time import sleep


class TestBaseModel(unittest.TestCase):
    """
    Test cases for the BaseModel class.
    """

    def setUp(self):
        """
        Set up method that will be called before each test.
        """
        self.model = BaseModel()

    def tearDown(self):
        """
        Tear down method that will be called after each test.
        """
        del self.model

    def test_id_creation(self):
        """
        Test that a unique id is created for each BaseModel instance.
        """
        model1 = BaseModel()
        model2 = BaseModel()
        self.assertNotEqual(model1.id, model2.id)

    def test_created_at_update(self):
        """
        Test that created_at attribute is updated when an instance is created.
        """
        self.assertIsNotNone(self.model.created_at)

    def test_updated_at_update(self):
        """
        Test that updated_at attribute is updated when an instance is created
        and when it is updated.
        """
        updated_at_prev = self.model.updated_at
        self.model.save()
        self.assertNotEqual(updated_at_prev, self.model.updated_at)

    def test_one_save(self):
        """
        Test that the updated_at attribute is updated after calling save().
        """
        instance = BaseModel()
        sleep(0.05)
        first_updated_at = instance.updated_at
        instance.save()
        self.assertLess(first_updated_at, instance.updated_at)

    def test_two_saves(self):
        """
        Test that the updated_at attribute is updated with multiple saves.
        """
        instance = BaseModel()
        sleep(0.05)
        first_updated_at = instance.updated_at
        instance.save()
        second_updated_at = instance.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        instance.save()
        self.assertLess(second_updated_at, instance.updated_at)

    def test_save_with_arg(self):
        """
        Test that passing an argument to save() raises a TypeError.
        """
        instance = BaseModel()
        with self.assertRaises(TypeError):
            instance.save(None)

    def test_save_updates_file(self):
        """
        Test that save() updates the file.
        """
        instance = BaseModel()
        instance.save()
        instanceid = "BaseModel." + instance.id
        with open("file.json", "r") as f:
            self.assertIn(instanceid, f.read())

    def test_to_dict_type(self):
        """
        Test the type of the returned dictionary from to_dict().
        """
        instance = BaseModel()
        self.assertTrue(dict, type(instance.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        """
        Test that the returned dictionary from
        to_dict() contains the correct keys.
        """
        instance = BaseModel()
        self.assertIn("id", instance.to_dict())
        self.assertIn("created_at", instance.to_dict())
        self.assertIn("updated_at", instance.to_dict())
        self.assertIn("__class__", instance.to_dict())

    def test_to_dict_contains_added_attributes(self):
        """
        Test that the returned dictionary from
        to_dict() contains added attributes.
        """
        instance = BaseModel()
        instance.name = "Holberton"
        instance.my_number = 98
        self.assertIn("name", instance.to_dict())
        self.assertIn("my_number", instance.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        """
        Test that the datetime attributes in the returned
        dictionary from to_dict() are of type string.
        """
        instance = BaseModel()
        instance_dict = instance.to_dict()
        self.assertEqual(str, type(instance_dict["created_at"]))
        self.assertEqual(str, type(instance_dict["updated_at"]))

    def test_to_dict_output(self):
        """
        Test the output of to_dict() against a predefined dictionary.
        """
        dt = datetime.today()
        instance = BaseModel()
        instance.id = "123456"
        instance.created_at = instance.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'BaseModel',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat()
        }
        self.assertDictEqual(instance.to_dict(), tdict)

    def test_contrast_to_dict_under_dict(self):
        """
        Test that the to_dict() method does not return the instance __dict__.
        """
        instance = BaseModel()
        self.assertNotEqual(instance.to_dict(), instance.__dict__)

    def test_to_dict_with_arg(self):
        """
        Test that passing an argument to to_dict() raises a TypeError.
        """
        instance = BaseModel()
        with self.assertRaises(TypeError):
            instance.to_dict(None)


if __name__ == "__main__":
    unittest.main()
