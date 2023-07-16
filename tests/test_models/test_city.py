#!/usr/bin/python3
"""Defines unittests for models/city.py.

Unittest classes:
    TestCityInstantiation
    TestCitySave
    TestCityToDict
"""

import unittest
from models.city import City
from models import storage
from time import sleep
from datetime import datetime


class TestCityInstantiation(unittest.TestCase):
    """Unittests for testing City instantiation."""

    def test_no_args_instantiates(self):
        self.assertEqual(City, type(City()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(City(), storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(City().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(City().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(City().updated_at))

    def test_state_id_is_public_class_attribute(self):
        city = City()
        self.assertEqual(str, type(City.state_id))
        self.assertIn("state_id", dir(city))
        self.assertNotIn("state_id", city.__dict__)

    def test_name_is_public_class_attribute(self):
        city = City()
        self.assertEqual(str, type(City.name))
        self.assertIn("name", dir(city))
        self.assertNotIn("name", city.__dict__)

    def test_two_cities_unique_ids(self):
        city_instance_1 = City()
        city_instance_2 = City()
        self.assertNotEqual(city_instance_1.id, city_instance_2.id)

    def test_two_cities_different_created_at(self):
        city_instance_1 = City()
        sleep(0.05)
        city_instance_2 = City()
        self.assertLess(city_instance_1.created_at, city_instance_2.created_at)

    def test_two_cities_different_updated_at(self):
        city_instance_1 = City()
        sleep(0.05)
        city_instance_2 = City()
        self.assertLess(city_instance_1.updated_at, city_instance_2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        city = City()
        city.id = "123456"
        city.created_at = city.updated_at = dt
        cstr = city.__str__()
        self.assertIn("[City] (123456)", cstr)
        self.assertIn("'id': '123456'", cstr)
        self.assertIn("'created_at': " + dt_repr, cstr)
        self.assertIn("'updated_at': " + dt_repr, cstr)

    def test_args_unused(self):
        city = City(None)
        self.assertNotIn(None, city.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        city = City(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(city.id, "345")
        self.assertEqual(city.created_at, dt)
        self.assertEqual(city.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)

    def test_instantiation(self):
        """Test that City instance is correctly instantiated."""
        city = City()
        self.assertIsInstance(city, City)
        self.assertIs(type(city), City)
        self.assertIsNotNone(city.id)
        self.assertIsNotNone(city.created_at)
        self.assertIsNotNone(city.updated_at)

    def test_attributes_initialization(self):
        """Test that City attributes are correctly initialized."""
        city = City()
        self.assertEqual(city.state_id, "")
        self.assertEqual(city.name, "")


class TestCitySave(unittest.TestCase):
    """Unittests for testing City save method."""

    def test_one_save(self):
        city_instance = City()
        sleep(0.05)
        first_updated_at = city_instance.updated_at
        city_instance.save()
        self.assertLess(first_updated_at, city_instance.updated_at)

    def test_two_saves(self):
        city_instance = City()
        sleep(0.05)
        first_updated_at = city_instance.updated_at
        city_instance.save()
        second_updated_at = city_instance.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        city_instance.save()
        self.assertLess(second_updated_at, city_instance.updated_at)

    def test_save_with_arg(self):
        city_instance = City()
        with self.assertRaises(TypeError):
            city_instance.save(None)

    def test_save_updates_file(self):
        city_instance = City()
        city_instance.save()
        city_id = "City." + city_instance.id
        with open("file.json", "r") as f:
            self.assertIn(city_id, f.read())

    def test_save_updates_updated_at(self):
        """Test that save method updates the updated_at attribute."""
        city = City()
        first_updated_at = city.updated_at
        city.save()
        self.assertNotEqual(first_updated_at, city.updated_at)


class TestCityToDict(unittest.TestCase):
    """Unittests for testing City to_dict method."""

    def test_to_dict_type(self):
        """Test the type of the returned dictionary from to_dict()."""
        city = City()
        self.assertTrue(dict, type(city.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        """Test that the returned dictionary from
        to_dict() contains the correct keys."""
        city = City()
        self.assertIn("id", city.to_dict())
        self.assertIn("created_at", city.to_dict())
        self.assertIn("updated_at", city.to_dict())
        self.assertIn("__class__", city.to_dict())

    def test_to_dict_contains_added_attributes(self):
        """Test that the returned dictionary from
        to_dict() contains added attributes."""
        city = City()
        city.state_id = "123"
        self.assertIn("state_id", city.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        """Test that the datetime attributes in the returned
        dictionary from to_dict() are of type string."""
        city = City()
        city_dict = city.to_dict()
        self.assertEqual(str, type(city_dict["created_at"]))
        self.assertEqual(str, type(city_dict["updated_at"]))

    def test_to_dict_output(self):
        """Test the output of to_dict() against a predefined dictionary."""
        dt = datetime.today()
        city = City()
        city.id = "123456"
        city.created_at = dt
        city.updated_at = dt
        city.state_id = "state_123"
        city.name = ""

        tdict = {
            'id': '123456',
            '__class__': 'City',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
            'state_id': 'state_123',
            'name': ""
        }

        self.assertDictEqual(city.to_dict(), tdict)

    def test_to_dict_with_arg(self):
        """Test that passing an argument to to_dict() raises a TypeError."""
        city = City()
        with self.assertRaises(TypeError):
            city.to_dict(None)


if __name__ == "__main__":
    unittest.main()
