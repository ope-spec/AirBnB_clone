#!/usr/bin/python3
"""Defines unittests for models/review.py.

Unittest classes:
    TestReviewInstantiation
    TestReviewSave
    TestReviewToDict
"""

import unittest
import os
from models.review import Review
from models import storage
from time import sleep
from datetime import datetime


class TestReviewInstantiation(unittest.TestCase):
    """Unittests for testing Review instantiation."""

    def test_no_args_instantiates(self):
        self.assertEqual(Review, type(Review()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Review(), storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Review().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Review().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Review().updated_at))

    def test_place_id_is_public_class_attribute(self):
        review = Review()
        self.assertEqual(str, type(Review.place_id))
        self.assertIn("place_id", dir(review))
        self.assertNotIn("place_id", review.__dict__)

    def test_user_id_is_public_class_attribute(self):
        review = Review()
        self.assertEqual(str, type(Review.user_id))
        self.assertIn("user_id", dir(review))
        self.assertNotIn("user_id", review.__dict__)

    def test_text_is_public_class_attribute(self):
        review = Review()
        self.assertEqual(str, type(Review.text))
        self.assertIn("text", dir(review))
        self.assertNotIn("text", review.__dict__)

    def test_two_reviews_unique_ids(self):
        review_instance_1 = Review()
        review_instance_2 = Review()
        self.assertNotEqual(review_instance_1.id, review_instance_2.id)

    def test_two_reviews_different_created_at(self):
        review_instance_1 = Review()
        sleep(0.05)
        review_instance_2 = Review()
        self.assertLess(
            review_instance_1.created_at,
            review_instance_2.created_at
        )

    def test_two_reviews_different_updated_at(self):
        review_instance_1 = Review()
        sleep(0.05)
        review_instance_2 = Review()
        self.assertLess(
            review_instance_1.updated_at,
            review_instance_2.updated_at
        )

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        review = Review()
        review.id = "123456"
        review.created_at = review.updated_at = dt
        rstr = review.__str__()
        self.assertIn("[Review] (123456)", rstr)
        self.assertIn("'id': '123456'", rstr)
        self.assertIn("'created_at': " + dt_repr, rstr)
        self.assertIn("'updated_at': " + dt_repr, rstr)

    def test_args_unused(self):
        review = Review(None)
        self.assertNotIn(None, review.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        review = Review(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(review.id, "345")
        self.assertEqual(review.created_at, dt)
        self.assertEqual(review.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)

    def test_instantiation(self):
        """Test that Review instance is correctly instantiated."""
        review = Review()
        self.assertIsInstance(review, Review)
        self.assertIs(type(review), Review)
        self.assertIsNotNone(review.id)
        self.assertIsNotNone(review.created_at)
        self.assertIsNotNone(review.updated_at)

    def test_attributes_initialization(self):
        """Test that Review attributes are correctly initialized."""
        review = Review()
        self.assertEqual(review.place_id, "")
        self.assertEqual(review.user_id, "")
        self.assertEqual(review.text, "")


class TestReviewSave(unittest.TestCase):
    """Unittests for testing Review save method."""

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
        review_instance = Review()
        sleep(0.05)
        first_updated_at = review_instance.updated_at
        review_instance.save()
        self.assertLess(first_updated_at, review_instance.updated_at)

    def test_two_saves(self):
        review_instance = Review()
        sleep(0.05)
        first_updated_at = review_instance.updated_at
        review_instance.save()
        second_updated_at = review_instance.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        review_instance.save()
        self.assertLess(second_updated_at, review_instance.updated_at)

    def test_save_with_arg(self):
        review_instance = Review()
        with self.assertRaises(TypeError):
            review_instance.save(None)

    def test_save_updates_file(self):
        review_instance = Review()
        review_instance.save()
        review_id = "Review." + review_instance.id
        with open("file.json", "r") as f:
            self.assertIn(review_id, f.read())

    def test_save_updates_updated_at(self):
        """Test that save method updates the updated_at attribute."""
        review = Review()
        first_updated_at = review.updated_at
        review.save()
        self.assertNotEqual(first_updated_at, review.updated_at)


class TestReviewToDict(unittest.TestCase):
    """Unittests for testing Review to_dict method."""

    def test_to_dict_type(self):
        """Test the type of the returned dictionary from to_dict()."""
        review = Review()
        self.assertTrue(dict, type(review.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        """Test that the returned dictionary from
        to_dict() contains the correct keys."""
        review = Review()
        self.assertIn("id", review.to_dict())
        self.assertIn("created_at", review.to_dict())
        self.assertIn("updated_at", review.to_dict())
        self.assertIn("__class__", review.to_dict())

    def test_to_dict_contains_added_attributes(self):
        """Test that the returned dictionary from
        to_dict() contains added attributes."""
        review = Review()
        review.place_id = "123"
        review.user_id = "456"
        self.assertIn("place_id", review.to_dict())
        self.assertIn("user_id", review.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        """Test that the datetime attributes in the returned
        dictionary from to_dict() are of type string."""
        review = Review()
        review_dict = review.to_dict()
        self.assertEqual(str, type(review_dict["created_at"]))
        self.assertEqual(str, type(review_dict["updated_at"]))

    def test_to_dict_output(self):
        """Test the output of to_dict() against a predefined dictionary."""
        dt = datetime.today()
        review = Review()
        review.id = "123456"
        review.created_at = dt
        review.updated_at = dt
        review.place_id = "789"
        review.user_id = "987"

        tdict = {
            'id': '123456',
            '__class__': 'Review',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
            'place_id': "789",
            'user_id': "987"
        }

        self.assertDictEqual(review.to_dict(), tdict)

    def test_to_dict_with_arg(self):
        """Test that passing an argument to to_dict() raises a TypeError."""
        review = Review()
        with self.assertRaises(TypeError):
            review.to_dict(None)


if __name__ == "__main__":
    unittest.main()
