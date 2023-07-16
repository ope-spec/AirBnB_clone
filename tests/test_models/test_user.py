#!/usr/bin/python3
"""Defines unittests for models/user.py.

Unittest classes:
    TestUserInstantiation
    TestUserSave
    TestUserToDict
"""

import unittest
from models.user import User
from models import storage
from datetime import datetime
from time import sleep


class TestUserInstantiation(unittest.TestCase):
    """Unittests for testing User instantiation."""

    def test_no_args_instantiates(self):
        self.assertEqual(User, type(User()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(User(), storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(User().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(User().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(User().updated_at))

    def test_email_is_public_str(self):
        self.assertEqual(str, type(User.email))

    def test_password_is_public_str(self):
        self.assertEqual(str, type(User.password))

    def test_first_name_is_public_str(self):
        self.assertEqual(str, type(User.first_name))

    def test_last_name_is_public_str(self):
        self.assertEqual(str, type(User.last_name))

    def test_two_users_unique_ids(self):
        user_instance_1 = User()
        user_instance_2 = User()
        self.assertNotEqual(user_instance_1.id, user_instance_2.id)

    def test_two_users_different_created_at(self):
        user_instance_1 = User()
        sleep(0.05)
        user_instance_2 = User()
        self.assertLess(user_instance_1.created_at, user_instance_2.created_at)

    def test_two_users_different_updated_at(self):
        user_instance_1 = User()
        sleep(0.05)
        user_instance_2 = User()
        self.assertLess(user_instance_1.updated_at, user_instance_2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        user = User()
        user.id = "123456"
        user.created_at = user.updated_at = dt
        usstr = user.__str__()
        self.assertIn("[User] (123456)", usstr)
        self.assertIn("'id': '123456'", usstr)
        self.assertIn("'created_at': " + dt_repr, usstr)
        self.assertIn("'updated_at': " + dt_repr, usstr)

    def test_args_unused(self):
        user = User(None)
        self.assertNotIn(None, user.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        user = User(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(user.id, "345")
        self.assertEqual(user.created_at, dt)
        self.assertEqual(user.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)


class TestUserSave(unittest.TestCase):
    """Unittests for testing User save method."""

    def test_one_save(self):
        user = User()
        sleep(0.05)
        first_updated_at = user.updated_at
        user.save()
        self.assertLess(first_updated_at, user.updated_at)

    def test_two_saves(self):
        user = User()
        sleep(0.05)
        first_updated_at = user.updated_at
        user.save()
        second_updated_at = user.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        user.save()
        self.assertLess(second_updated_at, user.updated_at)

    def test_save_with_arg(self):
        user = User()
        with self.assertRaises(TypeError):
            user.save(None)

    def test_save_updates_file(self):
        user = User()
        user.save()
        usid = "User." + user.id
        with open("file.json", "r") as f:
            self.assertIn(usid, f.read())

    def test_save_updates_updated_at(self):
        """Test that save method updates the updated_at attribute."""
        user = User()
        first_updated_at = user.updated_at
        user.save()
        self.assertNotEqual(first_updated_at, user.updated_at)


class TestUserToDict(unittest.TestCase):
    """Unittests for testing User to_dict method."""

    def test_to_dict_type(self):
        """Test the type of the returned dictionary from to_dict()."""
        user = User()
        self.assertTrue(dict, type(user.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        """Test that the returned dictionary from to_dict() contains the correct keys."""
        user = User()
        self.assertIn("id", user.to_dict())
        self.assertIn("created_at", user.to_dict())
        self.assertIn("updated_at", user.to_dict())
        self.assertIn("__class__", user.to_dict())

    def test_to_dict_contains_added_attributes(self):
        """Test that the returned dictionary from to_dict() contains added attributes."""
        user = User()
        user.email = "test@example.com"
        user.password = "password"
        user.first_name = "John"
        user.last_name = "Doe"
        self.assertIn("email", user.to_dict())
        self.assertIn("password", user.to_dict())
        self.assertIn("first_name", user.to_dict())
        self.assertIn("last_name", user.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        """Test that the datetime attributes in the returned dictionary from to_dict() are of type string."""
        user = User()
        user_dict = user.to_dict()
        self.assertEqual(str, type(user_dict["created_at"]))
        self.assertEqual(str, type(user_dict["updated_at"]))

    def test_to_dict_output(self):
        """Test the output of to_dict() against a predefined dictionary."""
        dt = datetime.today()
        user = User()
        user.id = "123456"
        user.created_at = dt
        user.updated_at = dt
        user.email = "test@example.com"
        user.password = "password"
        user.first_name = "John"
        user.last_name = "Doe"

        tdict = {
            'id': '123456',
            '__class__': 'User',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
            'email': "test@example.com",
            'password': "password",
            'first_name': "John",
            'last_name': "Doe"
        }

        self.assertDictEqual(user.to_dict(), tdict)

    def test_to_dict_with_arg(self):
        """Test that passing an argument to to_dict() raises a TypeError."""
        user = User()
        with self.assertRaises(TypeError):
            user.to_dict(None)


if __name__ == "__main__":
    unittest.main()
