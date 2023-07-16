#!/usr/bin/python3
"""Defines unittests for models/place.py.

Unittest classes:
    TestPlaceInstantiation
    TestPlaceSave
    TestPlaceToDict
"""

import unittest
import os
from models.place import Place
from models import storage
from time import sleep
from datetime import datetime


class TestPlaceInstantiation(unittest.TestCase):
    """Unittests for testing Place instantiation."""

    def test_no_args_instantiates(self):
        self.assertEqual(Place, type(Place()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Place(), storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Place().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Place().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Place().updated_at))

    def test_city_id_is_public_class_attribute(self):
        place = Place()
        self.assertEqual(str, type(Place.city_id))
        self.assertIn("city_id", dir(place))
        self.assertNotIn("city_id", place.__dict__)

    def test_user_id_is_public_class_attribute(self):
        place = Place()
        self.assertEqual(str, type(Place.user_id))
        self.assertIn("user_id", dir(place))
        self.assertNotIn("user_id", place.__dict__)

    def test_name_is_public_class_attribute(self):
        place = Place()
        self.assertEqual(str, type(Place.name))
        self.assertIn("name", dir(place))
        self.assertNotIn("name", place.__dict__)

    def test_description_is_public_class_attribute(self):
        place = Place()
        self.assertEqual(str, type(Place.description))
        self.assertIn("description", dir(place))
        self.assertNotIn("description", place.__dict__)

    def test_number_rooms_is_public_class_attribute(self):
        place = Place()
        self.assertEqual(int, type(Place.number_rooms))
        self.assertIn("number_rooms", dir(place))
        self.assertNotIn("number_rooms", place.__dict__)

    def test_number_bathrooms_is_public_class_attribute(self):
        place = Place()
        self.assertEqual(int, type(Place.number_bathrooms))
        self.assertIn("number_bathrooms", dir(place))
        self.assertNotIn("number_bathrooms", place.__dict__)

    def test_max_guest_is_public_class_attribute(self):
        place = Place()
        self.assertEqual(int, type(Place.max_guest))
        self.assertIn("max_guest", dir(place))
        self.assertNotIn("max_guest", place.__dict__)

    def test_price_by_night_is_public_class_attribute(self):
        place = Place()
        self.assertEqual(int, type(Place.price_by_night))
        self.assertIn("price_by_night", dir(place))
        self.assertNotIn("price_by_night", place.__dict__)

    def test_latitude_is_public_class_attribute(self):
        place = Place()
        self.assertEqual(float, type(Place.latitude))
        self.assertIn("latitude", dir(place))
        self.assertNotIn("latitude", place.__dict__)

    def test_longitude_is_public_class_attribute(self):
        place = Place()
        self.assertEqual(float, type(Place.longitude))
        self.assertIn("longitude", dir(place))
        self.assertNotIn("longitude", place.__dict__)

    def test_amenity_ids_is_public_class_attribute(self):
        place = Place()
        self.assertEqual(list, type(Place.amenity_ids))
        self.assertIn("amenity_ids", dir(place))
        self.assertNotIn("amenity_ids", place.__dict__)

    def test_two_places_unique_ids(self):
        place_instance_1 = Place()
        place_instance_2 = Place()
        self.assertNotEqual(
            place_instance_1.id,
            place_instance_2.id
        )

    def test_two_places_different_created_at(self):
        place_instance_1 = Place()
        sleep(0.05)
        place_instance_2 = Place()
        self.assertLess(
            place_instance_1.created_at,
            place_instance_2.created_at
        )

    def test_two_places_different_updated_at(self):
        place_instance_1 = Place()
        sleep(0.05)
        place_instance_2 = Place()
        self.assertLess(
            place_instance_1.updated_at,
            place_instance_2.updated_at
        )

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        place = Place()
        place.id = "123456"
        place.created_at = place.updated_at = dt
        pstr = place.__str__()
        self.assertIn("[Place] (123456)", pstr)
        self.assertIn("'id': '123456'", pstr)
        self.assertIn("'created_at': " + dt_repr, pstr)
        self.assertIn("'updated_at': " + dt_repr, pstr)

    def test_args_unused(self):
        place = Place(None)
        self.assertNotIn(None, place.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        place = Place(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(place.id, "345")
        self.assertEqual(place.created_at, dt)
        self.assertEqual(place.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Place(id=None, created_at=None, updated_at=None)

    def test_instantiation(self):
        """Test that Place instance is correctly instantiated."""
        place = Place()
        self.assertIsInstance(place, Place)
        self.assertIs(type(place), Place)
        self.assertIsNotNone(place.id)
        self.assertIsNotNone(place.created_at)
        self.assertIsNotNone(place.updated_at)

    def test_attributes_initialization(self):
        """Test that Place attributes are correctly initialized."""
        place = Place()
        self.assertEqual(place.city_id, "")
        self.assertEqual(place.user_id, "")
        self.assertEqual(place.name, "")
        self.assertEqual(place.description, "")
        self.assertEqual(place.number_rooms, 0)
        self.assertEqual(place.number_bathrooms, 0)
        self.assertEqual(place.max_guest, 0)
        self.assertEqual(place.price_by_night, 0)
        self.assertEqual(place.latitude, 0.0)
        self.assertEqual(place.longitude, 0.0)
        self.assertEqual(place.amenity_ids, [])


class TestPlaceSave(unittest.TestCase):
    """Unittests for testing Place save method."""

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
        place_instance = Place()
        sleep(0.05)
        first_updated_at = place_instance.updated_at
        place_instance.save()
        self.assertLess(first_updated_at, place_instance.updated_at)

    def test_two_saves(self):
        place_instance = Place()
        sleep(0.05)
        first_updated_at = place_instance.updated_at
        place_instance.save()
        second_updated_at = place_instance.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        place_instance.save()
        self.assertLess(second_updated_at, place_instance.updated_at)

    def test_save_with_arg(self):
        place_instance = Place()
        with self.assertRaises(TypeError):
            place_instance.save(None)

    def test_save_updates_file(self):
        place_instance = Place()
        place_instance.save()
        place_id = "Place." + place_instance.id
        with open("file.json", "r") as f:
            self.assertIn(place_id, f.read())

    def test_save_updates_updated_at(self):
        """Test that save method updates the updated_at attribute."""
        place = Place()
        first_updated_at = place.updated_at
        place.save()
        self.assertNotEqual(first_updated_at, place.updated_at)


class TestPlaceToDict(unittest.TestCase):
    """Unittests for testing Place to_dict method."""

    def test_to_dict_type(self):
        """Test the type of the returned dictionary from to_dict()."""
        place = Place()
        self.assertTrue(dict, type(place.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        """Test that the returned dictionary from
        to_dict() contains the correct keys."""
        place = Place()
        self.assertIn("id", place.to_dict())
        self.assertIn("created_at", place.to_dict())
        self.assertIn("updated_at", place.to_dict())
        self.assertIn("__class__", place.to_dict())

    def test_to_dict_contains_added_attributes(self):
        """Test that the returned dictionary from
        to_dict() contains added attributes."""
        place = Place()
        place.city_id = "123"
        place.user_id = "456"
        self.assertIn("city_id", place.to_dict())
        self.assertIn("user_id", place.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        """Test that the datetime attributes in the returned
        dictionary from to_dict() are of type string."""
        place = Place()
        place_dict = place.to_dict()
        self.assertEqual(str, type(place_dict["created_at"]))
        self.assertEqual(str, type(place_dict["updated_at"]))

    def test_to_dict_output(self):
        """Test the output of to_dict() against a predefined dictionary."""
        dt = datetime.today()
        place = Place()
        place.id = "123456"
        place.created_at = dt
        place.updated_at = dt
        place.city_id = "789"
        place.user_id = "987"

        tdict = {
            'id': '123456',
            '__class__': 'Place',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
            'city_id': "789",
            'user_id': "987"
        }

        self.assertDictEqual(place.to_dict(), tdict)

    def test_to_dict_with_arg(self):
        """Test that passing an argument to to_dict() raises a TypeError."""
        place = Place()
        with self.assertRaises(TypeError):
            place.to_dict(None)


if __name__ == "__main__":
    unittest.main()
