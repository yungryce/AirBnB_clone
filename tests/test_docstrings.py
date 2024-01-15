import unittest
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from datetime import datetime
from models.review import Review
from console import HBNBCommand


class TestDocstrings(unittest.TestCase):
    """Test case for checking docstrings"""

    MODULES_TO_TEST = [
        BaseModel,
        FileStorage,
        User,
        State,
        City,
        Amenity,
        Place,
        Review,
        HBNBCommand
        # Add other modules to test here
    ]

    def test_module_docstring(self):
        """Test module docstring"""
        for module_class in self.MODULES_TO_TEST:
            module = module_class.__module__
            self.assertIsNotNone(module.__doc__,
                                 f"Module docstring not found for {module}")
            self.assertNotEqual(len(module.__doc__.strip()), 0,
                                f"Empty docstring for {module}")

    def test_class_docstring(self):
        """Test class docstring"""
        for module_class in self.MODULES_TO_TEST:
            self.assertIsNotNone(
                module_class.__doc__,
                f"Class docstring not found for {module_class}"
                )
            self.assertNotEqual(
                len(module_class.__doc__.strip()),
                0,
                f"Empty class docstring for {module_class}"
                )

    def test_functions_docstrings(self):
        """Test functions docstrings"""
        excluded_methods = {'complete_help', 'completenames', 'get_names',
                            'print_topics'}

        for module_class in self.MODULES_TO_TEST:
            for func_name in dir(module_class):
                if (callable(getattr(module_class, func_name)) and
                        not func_name.startswith("__") and
                        func_name not in excluded_methods):
                    func = getattr(module_class, func_name)
                    self.assertIsNotNone(
                            func.__doc__,
                            f"Doc not found for {func_name} in {module_class}"
                            )
                    self.assertNotEqual(
                        len(func.__doc__.strip()),
                        0,
                        f"Empty docs for {func_name} in {module_class}"
                        )


if __name__ == "__main__":
    unittest.main()
