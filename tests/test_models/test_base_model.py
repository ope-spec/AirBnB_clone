#!/usr/bin/python3
"""Defines unittests for models/base_model.py.

Unittest classes:
    TestBaseModelInstantiation
    TestBaseModelSave
    TestBaseModelToDict
"""

import unittest
import os
from models.base_model import BaseModel
from models import storage
from time import sleep
from datetime import datetime


class TestBaseModelInstantiation(unittest.TestCase):
    """Unittests for testing BaseModel instantiation."""

    def test_no_args_instantiates(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(BaseModel(), storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(BaseModel().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_two_base_models_unique_ids(self):
        base_model_instance_1 = BaseModel()
        base_model_instance_2 = BaseModel()
        self.assertNotEqual(base_model_instance_1.id, base_model_instance_2.id)

    def test_two_base_models_different_created_at(self):
        base_model_instance_1 = BaseModel()
        sleep(0.05)
        base_model_instance_2 = BaseModel()
        self.assertLess(
            base_model_instance_1.created_at,
            base_model_instance_2.created_at
        )

    def test_two_base_models_different_updated_at(self):
        base_model_instance_1 = BaseModel()
        sleep(0.05)
        base_model_instance_2 = BaseModel()
        self.assertLess(
            base_model_instance_1.updated_at,
            base_model_instance_2.updated_at
        )

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        base_model = BaseModel()
        base_model.id = "123456"
        base_model.created_at = base_model.updated_at = dt
        bstr = base_model.__str__()
        self.assertIn("[BaseModel] (123456)", bstr)
        self.assertIn("'id': '123456'", bstr)
        self.assertIn("'created_at': " + dt_repr, bstr)
        self.assertIn("'updated_at': " + dt_repr, bstr)

    def test_args_unused(self):
        base_model = BaseModel(None)
        self.assertNotIn(None, base_model.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        base_model = BaseModel(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(base_model.id, "345")
        self.assertEqual(base_model.created_at, dt)
        self.assertEqual(base_model.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_instantiation(self):
        """Test that BaseModel instance is correctly instantiated."""
        base_model = BaseModel()
        self.assertIsInstance(base_model, BaseModel)
        self.assertIs(type(base_model), BaseModel)
        self.assertIsNotNone(base_model.id)
        self.assertIsNotNone(base_model.created_at)
        self.assertIsNotNone(base_model.updated_at)


class TestBaseModelSave(unittest.TestCase):
    """Unittests for testing BaseModel save method."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        base_model_instance = BaseModel()
        sleep(0.05)
        first_updated_at = base_model_instance.updated_at
        base_model_instance.save()
        self.assertLess(first_updated_at, base_model_instance.updated_at)

    def test_two_saves(self):
        base_model_instance = BaseModel()
        sleep(0.05)
        first_updated_at = base_model_instance.updated_at
        base_model_instance.save()
        second_updated_at = base_model_instance.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        base_model_instance.save()
        self.assertLess(second_updated_at, base_model_instance.updated_at)

    def test_save_with_arg(self):
        base_model_instance = BaseModel()
        with self.assertRaises(TypeError):
            base_model_instance.save(None)

    def test_save_updates_file(self):
        base_model_instance = BaseModel()
        base_model_instance.save()
        base_model_id = "BaseModel." + base_model_instance.id
        with open("file.json", "r") as f:
            self.assertIn(base_model_id, f.read())

    def test_save_updates_updated_at(self):
        """Test that save method updates the updated_at attribute."""
        base_model = BaseModel()
        first_updated_at = base_model.updated_at
        base_model.save()
        self.assertNotEqual(first_updated_at, base_model.updated_at)


class TestBaseModelToDict(unittest.TestCase):
    """Unittests for testing BaseModel to_dict method."""

    def test_to_dict_type(self):
        """Test the type of the returned dictionary from to_dict()."""
        base_model = BaseModel()
        self.assertTrue(dict, type(base_model.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        """Test that the returned dictionary from
        to_dict() contains the correct keys."""
        base_model = BaseModel()
        self.assertIn("id", base_model.to_dict())
        self.assertIn("created_at", base_model.to_dict())
        self.assertIn("updated_at", base_model.to_dict())
        self.assertIn("__class__", base_model.to_dict())

    def test_to_dict_contains_added_attributes(self):
        """Test that the returned dictionary from
        to_dict() contains added attributes."""
        base_model = BaseModel()
        base_model.name = "test"
        base_model.number = 123
        self.assertIn("name", base_model.to_dict())
        self.assertIn("number", base_model.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        """Test that the datetime attributes in the returned
        dictionary from to_dict() are of type string."""
        base_model = BaseModel()
        base_model_dict = base_model.to_dict()
        self.assertEqual(str, type(base_model_dict["created_at"]))
        self.assertEqual(str, type(base_model_dict["updated_at"]))

    def test_to_dict_output(self):
        """Test the output of to_dict() against a predefined dictionary."""
        dt = datetime.today()
        base_model = BaseModel()
        base_model.id = "123456"
        base_model.created_at = dt
        base_model.updated_at = dt
        base_model.name = "test"
        base_model.number = 123

        tdict = {
            'id': '123456',
            '__class__': 'BaseModel',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
            'name': 'test',
            'number': 123
        }

        self.assertDictEqual(base_model.to_dict(), tdict)

    def test_to_dict_with_arg(self):
        """Test that passing an argument to to_dict() raises a TypeError."""
        base_model = BaseModel()
        with self.assertRaises(TypeError):
            base_model.to_dict(None)


if __name__ == "__main__":
    unittest.main()
