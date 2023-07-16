#!/usr/bin/python3
"""Defines unittests for models/state.py.

Unittest classes:
    TestStateInstantiation
    TestStateSave
    TestStateToDict
"""

import unittest
from models.state import State
from models import storage
from time import sleep
from datetime import datetime


class TestStateInstantiation(unittest.TestCase):
    """Unittests for testing State instantiation."""

    def test_no_args_instantiates(self):
        self.assertEqual(State, type(State()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(State(), storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(State().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(State().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(State().updated_at))

    def test_name_is_public_class_attribute(self):
        state = State()
        self.assertEqual(str, type(State.name))
        self.assertIn("name", dir(state))
        self.assertNotIn("name", state.__dict__)

    def test_two_states_unique_ids(self):
        state_instance_1 = State()
        state_instance_2 = State()
        self.assertNotEqual(state_instance_1.id, state_instance_2.id)

    def test_two_states_different_created_at(self):
        state_instance_1 = State()
        sleep(0.05)
        state_instance_2 = State()
        self.assertLess(
            state_instance_1.created_at,
            state_instance_2.created_at
        )

    def test_two_states_different_updated_at(self):
        state_instance_1 = State()
        sleep(0.05)
        state_instance_2 = State()
        self.assertLess(
            state_instance_1.updated_at,
            state_instance_2.updated_at
        )

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        state = State()
        state.id = "123456"
        state.created_at = state.updated_at = dt
        ststr = state.__str__()
        self.assertIn("[State] (123456)", ststr)
        self.assertIn("'id': '123456'", ststr)
        self.assertIn("'created_at': " + dt_repr, ststr)
        self.assertIn("'updated_at': " + dt_repr, ststr)

    def test_args_unused(self):
        state = State(None)
        self.assertNotIn(None, state.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        state = State(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(state.id, "345")
        self.assertEqual(state.created_at, dt)
        self.assertEqual(state.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)

    def test_instantiation(self):
        """Test that State instance is correctly instantiated."""
        state = State()
        self.assertIsInstance(state, State)
        self.assertIs(type(state), State)
        self.assertIsNotNone(state.id)
        self.assertIsNotNone(state.created_at)
        self.assertIsNotNone(state.updated_at)

    def test_attributes_initialization(self):
        """Test that State attributes are correctly initialized."""
        state = State()
        self.assertEqual(state.name, "")


class TestStateSave(unittest.TestCase):
    """Unittests for testing State save method."""

    def test_one_save(self):
        state_instance = State()
        sleep(0.05)
        first_updated_at = state_instance.updated_at
        state_instance.save()
        self.assertLess(first_updated_at, state_instance.updated_at)

    def test_two_saves(self):
        state_instance = State()
        sleep(0.05)
        first_updated_at = state_instance.updated_at
        state_instance.save()
        second_updated_at = state_instance.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        state_instance.save()
        self.assertLess(second_updated_at, state_instance.updated_at)

    def test_save_with_arg(self):
        state_instance = State()
        with self.assertRaises(TypeError):
            state_instance.save(None)

    def test_save_updates_file(self):
        state_instance = State()
        state_instance.save()
        stid = "State." + state_instance.id
        with open("file.json", "r") as f:
            self.assertIn(stid, f.read())

    def test_save_updates_updated_at(self):
        """Test that save method updates the updated_at attribute."""
        state = State()
        first_updated_at = state.updated_at
        state.save()
        self.assertNotEqual(first_updated_at, state.updated_at)


class TestStateToDict(unittest.TestCase):
    """Unittests for testing State to_dict method."""

    def test_to_dict_type(self):
        """Test the type of the returned dictionary from to_dict()."""
        state = State()
        self.assertTrue(dict, type(state.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        """Test that the returned dictionary from
        to_dict() contains the correct keys."""
        state = State()
        self.assertIn("id", state.to_dict())
        self.assertIn("created_at", state.to_dict())
        self.assertIn("updated_at", state.to_dict())
        self.assertIn("__class__", state.to_dict())

    def test_to_dict_contains_added_attributes(self):
        """Test that the returned dictionary from
        to_dict() contains added attributes."""
        state = State()
        state.name = "California"
        self.assertIn("name", state.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        """Test that the datetime attributes in the returned
        dictionary from to_dict() are of type string."""
        state = State()
        state_dict = state.to_dict()
        self.assertEqual(str, type(state_dict["created_at"]))
        self.assertEqual(str, type(state_dict["updated_at"]))

    def test_to_dict_output(self):
        """Test the output of to_dict() against a predefined dictionary."""
        dt = datetime.today()
        state = State()
        state.id = "123456"
        state.created_at = dt
        state.updated_at = dt
        state.name = ""

        tdict = {
            'id': '123456',
            '__class__': 'State',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
            'name': ""
        }

        self.assertDictEqual(state.to_dict(), tdict)

    def test_to_dict_with_arg(self):
        """Test that passing an argument to to_dict() raises a TypeError."""
        state = State()
        with self.assertRaises(TypeError):
            state.to_dict(None)


if __name__ == "__main__":
    unittest.main()
