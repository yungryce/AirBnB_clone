""" pycodestyle tests """
import unittest
import pycodestyle

class TestCodeStyle(unittest.TestCase):
    """test case for pycodestyle"""

    def test_BaseModel(self):
        """ test for pep8 conformance"""
        style = pycodestyle.StyleGuide(quiet=False)
        result = style.check_files([
            "models/__init__.py",
            "models/engine/file_storage.py",
            "models/base_model.py",
            "console.py",
            "tests/test_models/test_base_model.py"
        ])
        self.assertEqual(result.total_errors, 0, "PEP 8 style issues found")

        
if __name__ == "__main__":
    unittest.main()
