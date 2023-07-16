#!/usr/bin/python3
"""Defines unittests for models/amenity.py.

Unittest classes:
    TestAmenityInstantiation
    TestAmenitySave
    TestAmenityToDict
"""

import unittest
import os
from models.amenity import Amenity
from models import storage
from time import sleep
from datetime import datetime


class TestAmenityInstantiation(unittest.TestCase):
    """Unittests for testing Amenity instantiation."""

    def test_no_args_instantiates(self):
        self.assertEqual(Amenity, type(Amenity()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Amenity(), storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Amenity().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().updated_at))

    def test_name_is_public_class_attribute(self):
        amenity = Amenity()
        self.assertEqual(str, type(Amenity.name))
        self.assertIn("name", dir(amenity))
        self.assertNotIn("name", amenity.__dict__)

    def test_two_amenities_unique_ids(self):
        amenity_instance_1 = Amenity()
        amenity_instance_2 = Amenity()
        self.assertNotEqual(amenity_instance_1.id, amenity_instance_2.id)

    def test_two_amenities_different_created_at(self):
        amenity_instance_1 = Amenity()
        sleep(0.05)
        amenity_instance_2 = Amenity()
        self.assertLess(
            amenity_instance_1.created_at,
            amenity_instance_2.created_at
        )

    def test_two_amenities_different_updated_at(self):
        amenity_instance_1 = Amenity()
        sleep(0.05)
        amenity_instance_2 = Amenity()
        self.assertLess(
            amenity_instance_1.updated_at,
            amenity_instance_2.updated_at
        )

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        amenity = Amenity()
        amenity.id = "123456"
        amenity.created_at = amenity.updated_at = dt
        astr = amenity.__str__()
        self.assertIn("[Amenity] (123456)", astr)
        self.assertIn("'id': '123456'", astr)
        self.assertIn("'created_at': " + dt_repr, astr)
        self.assertIn("'updated_at': " + dt_repr, astr)

    def test_args_unused(self):
        amenity = Amenity(None)
        self.assertNotIn(None, amenity.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        amenity = Amenity(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(amenity.id, "345")
        self.assertEqual(amenity.created_at, dt)
        self.assertEqual(amenity.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)

    def test_instantiation(self):
        """Test that Amenity instance is correctly instantiated."""
        amenity = Amenity()
        self.assertIsInstance(amenity, Amenity)
        self.assertIs(type(amenity), Amenity)
        self.assertIsNotNone(amenity.id)
        self.assertIsNotNone(amenity.created_at)
        self.assertIsNotNone(amenity.updated_at)

    def test_attributes_initialization(self):
        """Test that Amenity attributes are correctly initialized."""
        amenity = Amenity()
        self.assertEqual(amenity.name, "")


class TestAmenitySave(unittest.TestCase):
    """Unittests for testing Amenity save method."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

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
        amenity_instance = Amenity()
        sleep(0.05)
        first_updated_at = amenity_instance.updated_at
        amenity_instance.save()
        self.assertLess(first_updated_at, amenity_instance.updated_at)

    def test_two_saves(self):
        amenity_instance = Amenity()
        sleep(0.05)
        first_updated_at = amenity_instance.updated_at
        amenity_instance.save()
        second_updated_at = amenity_instance.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        amenity_instance.save()
        self.assertLess(second_updated_at, amenity_instance.updated_at)

    def test_save_with_arg(self):
        amenity_instance = Amenity()
        with self.assertRaises(TypeError):
            amenity_instance.save(None)

    def test_save_updates_file(self):
        amenity_instance = Amenity()
        amenity_instance.save()
        amenity_id = "Amenity." + amenity_instance.id
        with open("file.json", "r") as f:
            self.assertIn(amenity_id, f.read())

    def test_save_updates_updated_at(self):
        """Test that save method updates the updated_at attribute."""
        amenity = Amenity()
        first_updated_at = amenity.updated_at
        amenity.save()
        self.assertNotEqual(first_updated_at, amenity.updated_at)


class TestAmenityToDict(unittest.TestCase):
    """Unittests for testing Amenity to_dict method."""

    def test_to_dict_type(self):
        """Test the type of the returned dictionary from to_dict()."""
        amenity = Amenity()
        self.assertTrue(dict, type(amenity.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        """Test that the returned dictionary from
        to_dict() contains the correct keys."""
        amenity = Amenity()
        self.assertIn("id", amenity.to_dict())
        self.assertIn("created_at", amenity.to_dict())
        self.assertIn("updated_at", amenity.to_dict())
        self.assertIn("__class__", amenity.to_dict())

    def test_to_dict_contains_added_attributes(self):
        """Test that the returned dictionary from
        to_dict() contains added attributes."""
        amenity = Amenity()
        amenity.name = "WiFi"
        self.assertIn("name", amenity.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        """Test that the datetime attributes in the returned
        dictionary from to_dict() are of type string."""
        amenity = Amenity()
        amenity_dict = amenity.to_dict()
        self.assertEqual(str, type(amenity_dict["created_at"]))
        self.assertEqual(str, type(amenity_dict["updated_at"]))

    def test_to_dict_output(self):
        """Test the output of to_dict() against a predefined dictionary."""
        dt = datetime.today()
        amenity = Amenity()
        amenity.id = "123456"
        amenity.created_at = dt
        amenity.updated_at = dt
        amenity.name = "WiFi"

        tdict = {
            'id': '123456',
            '__class__': 'Amenity',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
            'name': "WiFi"
        }

        self.assertDictEqual(amenity.to_dict(), tdict)

    def test_to_dict_with_arg(self):
        """Test that passing an argument to to_dict() raises a TypeError."""
        amenity = Amenity()
        with self.assertRaises(TypeError):
            amenity.to_dict(None)


if __name__ == "__main__":
    unittest.main()
