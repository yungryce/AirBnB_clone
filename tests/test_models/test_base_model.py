""" Unit tests for BaseModel class """

import unittest
from models.base_model import BaseModel
from datetime import datetime, timedelta
from unittest.mock import patch
from uuid import uuid4


class TestBaseModel(unittest.TestCase):
    """test case for BaseModel"""

    def assertBaseModelAttributes(self, obj, id_check=True):
        """Assert common attributes of BaseModel"""
        self.assertIsNotNone(obj.id, "ID should not be None")
        self.assertIsInstance(obj.id, str, "ID should be of type str")
        self.assertIsInstance(obj.created_at, datetime, "Type of datetime")
        self.assertIsInstance(obj.updated_at, datetime, "Type of datetime")
        self.assertEqual(type(obj), BaseModel, "Type of object BaseModel")
        if id_check:
            self.assertNotEqual(obj.id, "", "ID should not be an empty string")

    def test_base_model_initialization(self):
        """Test the initialization of BaseModel"""

        # Assertions for the first instance (a1)
        a1 = BaseModel()
        self.assertBaseModelAttributes(a1)

        # Assertions for the second instance (a2)
        a2_uuid = str(uuid4())
        a2 = BaseModel()
        a2.id = a2_uuid
        a2.name = "My Second Model"
        a2.my_number = 89
        self.assertBaseModelAttributes(a2)
        self.assertEqual(a2_uuid, a2.id, "ID should match assigned value")
        self.assertEqual(a2.name, "My Second Model", "name shall match value")
        self.assertEqual(a2.my_number, 89, "my_number should match value")
        self.assertIn("name", a2.__dict__, "name should be in __dict__")
        self.assertIn("my_number", a2.__dict__, "my_number be in __dict__")

        # Assertions for the third instance (a3)
        a3_uuid = str(uuid4())
        a3 = BaseModel(id=a3_uuid, name="My third Model", my_number=9)
        self.assertBaseModelAttributes(a3)
        self.assertEqual(a3_uuid, a3.id, "ID should match assigned value")
        self.assertEqual(a2.name, "My Second Model", "name shall match value")
        self.assertEqual(a2.my_number, 89, "my_number should match value")
        self.assertIn("name", a3.__dict__, "name should be in __dict__")
        self.assertIn("my_number", a3.__dict__, "my_number in __dict__")

        # Test for inequality
        self.assertNotEqual(a1.id, a2.id, a3.id)

    def test_base_model_init_with_kwargs(self):
        """Test BaseModel initialization with kwargs"""

        # Test case 1: Pass all valid kwargs
        obj1_kwargs = {
            'id': str(uuid4()),
            'created_at': '2022-01-01T12:00:00',
            'updated_at': '2022-01-01T13:00:00',
            'custom_attr': 'custom_value'
        }
        obj1 = BaseModel(**obj1_kwargs)
        self.assertBaseModelAttributes(obj1, id_check=False)
        self.assertEqual(obj1.id, obj1_kwargs["id"])
        self.assertEqual(obj1.created_at,
                         datetime.fromisoformat('2022-01-01T12:00:00'))
        self.assertEqual(obj1.updated_at,
                         datetime.fromisoformat('2022-01-01T13:00:00'))
        self.assertEqual(obj1.custom_attr, 'custom_value')

        # Test case 2: Pass invalid kwargs (excluding '__class__')
        obj2_kwargs = {
            'invalid_attr': 'invalid_value',
            '__class__': 'InvalidClass'
            }
        obj2 = BaseModel(**obj2_kwargs)
        self.assertBaseModelAttributes(obj2)

    def test_base_model_init_with_empty_kwargs(self):
        """Test BaseModel initialization with empty kwargs"""
        obj = BaseModel(**{})
        self.assertBaseModelAttributes(obj)

    def test_base_model_init_without_kwargs(self):
        """Test BaseModel initialization without kwargs"""
        obj = BaseModel()
        self.assertBaseModelAttributes(obj)

    def test_base_model_init_invalid_datetime_format(self):
        """Test BaseModel init with invalid datetime format in kwargs"""
        invalid_datetime_kwargs = {'created_at': 'invalid_format'}
        with self.assertRaises(ValueError):
            BaseModel(**invalid_datetime_kwargs)

    def test_str(self):
        """ Test the __str__ method of BaseModel """
        a4 = BaseModel()
        expected_str = f"[{a4.__class__.__name__}] ({a4.id}) {a4.__dict__}"
        self.assertEqual(str(a4), expected_str)

    def test_dict(self):
        """Test method for dict"""
        a5 = BaseModel()
        a5_dict = a5.to_dict()
        self.assertIsInstance(a5_dict, dict)
        self.assertIn('id', a5_dict.keys())
        self.assertIn('created_at', a5_dict.keys())
        self.assertIn('updated_at', a5_dict.keys())
        self.assertEqual(a5_dict['__class__'], type(a5).__name__)

        # assetion for exception
        a6_uuid = str(uuid4())
        a6 = BaseModel(id=a6_uuid, name="My third Model", my_number=9)
        a6_dict = a6.to_dict()
        self.assertIn('name', a6_dict.keys())
        self.assertIn('my_number', a6_dict.keys())
        self.assertEqual(a6.id, a6_uuid)

    def test_base_model_to_dict_with_custom_attrs(self):
        """Test the to_dict method of BaseModel with custom attributes"""
        obj = BaseModel(id='123', created_at='2022-01-01T12:00:00',
                        updated_at='2022-01-01T13:00:00')
        obj.custom_attr = 'custom_value'
        obj_dict = obj.to_dict()

        self.assertIn('custom_attr', obj_dict)
        self.assertEqual(obj_dict['custom_attr'], 'custom_value')

    def test_base_model_to_dict_with_empty_attrs(self):
        """Test the to_dict method of BaseModel with empty attributes"""
        obj = BaseModel()
        obj_dict = obj.to_dict()

        self.assertNotIn('custom_attr', obj_dict)

    def test_base_model_to_dict_with_invalid_datetime_format(self):
        """Test the to_dict method of BaseModel with invalid datetime format"""
        with self.assertRaises(ValueError) as context:
            obj = BaseModel(created_at='invalid_format')
            obj_dict = obj.to_dict()

    def test_base_model_save(self):
        """Test the save method of BaseModel"""
        obj = BaseModel()
        original_updated_at = obj.updated_at

        with patch('models.storage.save') as mock_save:
            obj.save()

        self.assertNotEqual(original_updated_at, obj.updated_at)
        self.assertTrue(mock_save.called)

    def test_base_model_save_multiple_calls(self):
        """Test multiple calls to the save method of BaseModel"""
        obj = BaseModel()
        original_updated_at = obj.updated_at

        with patch('models.storage.save') as mock_save:
            obj.save()
            obj.save()

        self.assertNotEqual(original_updated_at, obj.updated_at)
        self.assertEqual(mock_save.call_count, 2)

    def test_base_model_save_after_custom_datetime(self):
        """Test save method of BaseModel after updating custom datetime"""
        obj = BaseModel()
        custom_datetime = datetime.now() - timedelta(days=1)
        obj.updated_at = custom_datetime

        with patch('models.storage.save') as mock_save:
            obj.save()

        self.assertNotEqual(custom_datetime, obj.updated_at)
        self.assertTrue(mock_save.called)


if __name__ == "__main__":
    unittest.main()
