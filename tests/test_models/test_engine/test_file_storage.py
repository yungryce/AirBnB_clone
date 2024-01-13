import unittest
import os
import json
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):
    """Test case for FileStorage"""

    def setUp(self):
        """Set up for testing"""
        self.file_path = "test_file.json"
        self.storage = FileStorage()
        self.storage._FileStorage__objects = {}
        self.storage._FileStorage__file_path = self.file_path

    def tearDown(self):
        """Clean up after testing"""
        self.storage._FileStorage__objects = {}
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_all_empty(self):
        """Test all method with an empty storage"""
        all_objects = self.storage.all()
        self.assertIsInstance(all_objects, dict)
        self.assertEqual(len(all_objects), 0)

    def test_new_and_all(self):
        """Test new and all methods"""
        obj1 = BaseModel()
        self.storage.new(obj1)
        all_objects = self.storage.all()
        self.assertEqual(len(all_objects), 1)
        self.assertIn(f"{obj1.__class__.__name__}.{obj1.id}", all_objects)

    def test_save_and_reload(self):
        """Test save and reload methods"""
        obj1 = BaseModel()
        obj2 = BaseModel()
        self.storage.new(obj1)
        self.storage.new(obj2)
        self.storage.save()

        # Check if file exists
        self.assertTrue(os.path.exists(self.file_path))

        # Clear objects, reload, and check if they match
        self.storage._FileStorage__objects = {}
        self.storage.reload()
        reloaded_objects = self.storage.all()

        self.assertEqual(len(reloaded_objects), 2)
        self.assertIn(f"{obj1.__class__.__name__}.{obj1.id}", reloaded_objects)
        self.assertIn(f"{obj2.__class__.__name__}.{obj2.id}", reloaded_objects)

    def test_reload_nonexistent_file(self):
        """Test reload method with nonexistent file"""
        self.storage._FileStorage__objects = {}
        self.storage.reload()  # This should not raise an exception

    def test_reload_invalid_json(self):
        """Test reload method with invalid JSON"""
        with open(self.file_path, "w") as file:
            file.write("invalid_json")

        # The reload should not raise an exception but should not load anything
        self.storage.reload()
        reloaded_objects = self.storage.all()
        self.assertEqual(len(reloaded_objects), 0)


if __name__ == "__main__":
    unittest.main()
