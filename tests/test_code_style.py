""" pycodestyle tests """
import unittest
import pycodestyle

FILES_TO_CHECK = [
    "models/__init__.py",
    "models/engine/file_storage.py",
    "models/base_model.py",
    "models/user.py",
    "models/state.py",
    "models/city.py",
    "models/amenity.py",
    "models/place.py",
    "models/review.py",
    "console.py",
    "tests/test_models/test_base_model.py",
    "tests/test_console.py",
    "tests/test_docstrings.py",
    "tests/test_code_style.py",
    "tests/test_models/test_engine/test_file_storage.py",
    "tests/test_models/test_user.py",
    "tests/test_models/test_state.py",
    "tests/test_models/test_city.py",
    "tests/test_models/test_amenity.py",
    "tests/test_models/test_place.py",
    "tests/test_models/test_review.py"
]


class TestCodeStyle(unittest.TestCase):
    """test case for pycodestyle"""

    def test_files(self):
        """ test for pep8 conformance"""
        style = pycodestyle.StyleGuide(quiet=False)
        result = style.check_files(FILES_TO_CHECK)
        self.assertEqual(result.total_errors, 0, "PEP 8 style issues found")


if __name__ == "__main__":
    unittest.main()
