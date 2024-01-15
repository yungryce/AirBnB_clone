import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand, validate_classname, validate_attrs
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from console import current_classes


class TestHBNBCommand(unittest.TestCase):
    """Test class for the HBNBCommand class."""

    def setUp(self):
        """Set up resources needed for the tests."""
        self.mock_stdout = StringIO()

    def tearDown(self):
        """Tear down resources after the tests."""
        self.mock_stdout.close()

    def assert_output(self, expected_output, function, *args):
        """
        Assert the output of a function matches the expected output.

        Args:
            expected_output (str): The expected output.
            function (callable): The function to test.
            *args: Variable length argument list to pass to the function.

        Raises:
            AssertionError: If the output does not match the expected output.
        """
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            function(*args)
            self.assertEqual(mock_stdout.getvalue().strip(), expected_output)

    def test_quit_command(self):
        """Test the do_quit method."""
        self.assertTrue(HBNBCommand().onecmd("quit"))

    def test_EOF_command(self):
        """Test the do_EOF method."""
        self.assertTrue(HBNBCommand().onecmd("EOF"))

    def test_emptyline_command(self):
        """Test the emptyline method."""
        self.assert_output("", HBNBCommand().onecmd, "")


class TestPreCmdMethod(unittest.TestCase):

    def setUp(self):
        """Set up resources needed for the tests."""
        self.mock_stdout = StringIO()

    def tearDown(self):
        """Tear down resources after the tests."""
        self.mock_stdout.close()

    def assert_output(self, expected_output, function, *args):
        """Assert the output of a function matches the expected output."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            function(*args)
            self.assertEqual(mock_stdout.getvalue().strip(), expected_output)

    def test_precmd_empty_string(self):
        """test precmd method with empty string"""
        result = HBNBCommand().precmd('')
        self.assertEqual('\n', result)

    def test_precmd_no_match(self):
        """test precmd method with no match"""
        result = HBNBCommand().precmd('invalid_syntax')
        self.assertEqual('invalid_syntax', result)

    def test_precmd_invalid_method(self):
        """test precmd method with invalid method"""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            result = HBNBCommand().precmd('User.invalid_method()')
        self.assertEqual('\n', result)
        self.assertEqual('', mock_stdout.getvalue().strip())

    def test_precmd_valid_method_no_args(self):
        """test precmd method with valid method and no args"""
        result = HBNBCommand().precmd('User.count()')
        self.assertEqual('\n', result)

    def test_precmd_valid_method_with_args(self):
        """test precmd method with valid method and args"""
        result = HBNBCommand().precmd('User.update("123", name, "John Doe")')
        self.assertEqual('\n', result)

    def test_precmd_valid_method_with_dict_arg(self):
        """test precmd method with valid method and dict arg"""""
        result = HBNBCommand().precmd(
            'User.update("123", {"name": "John Doe"})')
        self.assertEqual('\n', result)

    def test_precmd_valid_method_with_uuid_arg(self):
        """test precmd method with valid method and uuid arg"""
        result = HBNBCommand().precmd(
            'User.update("123", "uuid_here", {"name": "John Doe"})')
        self.assertEqual('\n', result)

    def test_precmd_valid_method_with_space_in_arg(self):
        """test precmd method with valid method and space in arg"""
        result = HBNBCommand().precmd(
            'User.update("123", name, "John Doe with space")')
        self.assertEqual('\n', result)

    def test_precmd_valid_method_with_spaces_in_attr_value(self):
        """test precmd method with valid method and spaces in attr value"""
        result = HBNBCommand().precmd(
            'User.update("123", name, "John Doe", '
            '{"attr": "value with spaces"})')
        self.assertEqual('\n', result)

    def test_precmd_special_characters(self):
        """test precmd method with special characters"""
        result = HBNBCommand().precmd(
            'User.update("!@#^&*()_+{}[]", name, "Special chars")')
        self.assertEqual('\n', result)

    def test_precmd_edge_case_spaces_in_attr_name(self):
        """test precmd method with edge case spaces in attr name"""
        result = HBNBCommand().precmd(
            'User.update("123", name, "John Doe", '
            '{"attr with space": "value"})')
        self.assertEqual('\n', result)

    def test_precmd_edge_case_empty_string_as_attr_value(self):
        """test precmd method with edge case empty string as attr value"""
        result = HBNBCommand().precmd(
            'User.update("123", name, "John Doe", {"attr": ""})')
        self.assertEqual('\n', result)


class TestCreateMethod(unittest.TestCase):
    """Test class for the do_create() method of the HBNBCommand class."""

    def setUp(self):
        """Set up resources needed for the tests."""
        self.mock_stdout = StringIO()

    def tearDown(self):
        """Tear down resources after the tests."""
        self.mock_stdout.close()

    def test_do_create_valid_classname(self):
        """Test do_create with a valid class name."""
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertLess(0, len(mock_stdout.getvalue().strip()))
            testKey = "BaseModel.{}".format(mock_stdout.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())

    def test_do_create_invalid_classname(self):
        """Test do_create with an invalid class name."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            HBNBCommand().do_create('InvalidClassName')
        self.assertEqual(
            '** class doesn\'t exist **', mock_stdout.getvalue().strip())

    def test_do_create_missing_classname(self):
        """Test do_create with missing class name."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            HBNBCommand().do_create('')
        self.assertEqual(
            '** class name missing **', mock_stdout.getvalue().strip())

    def test_do_create_extra_arguments(self):
        """Test do_create with extra arguments."""
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel exa_arg"))
            testKey = "BaseModel.{}".format(mock_stdout.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())

    def test_do_create_user(self):
        """Test do_create with User class."""
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertLess(0, len(mock_stdout.getvalue().strip()))
            testKey = "User.{}".format(mock_stdout.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())

    def test_do_create_state(self):
        """Test do_create with State class."""
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertLess(0, len(mock_stdout.getvalue().strip()))
            testKey = "State.{}".format(mock_stdout.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())

    def test_do_create_city(self):
        """Test do_create with City class."""
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertLess(0, len(mock_stdout.getvalue().strip()))
            testKey = "City.{}".format(mock_stdout.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())

    def test_do_create_amenity(self):
        """Test do_create with Amenity class."""
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertLess(0, len(mock_stdout.getvalue().strip()))
            testKey = "Amenity.{}".format(mock_stdout.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())

    def test_do_create_place(self):
        """Test do_create with Place class."""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertLess(0, len(mock_stdout.getvalue().strip()))
            testKey = "Place.{}".format(mock_stdout.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())

    def test_do_create_review(self):
        """Test do_create with Review class."""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            self.assertLess(0, len(mock_stdout.getvalue().strip()))
            testKey = "Review.{}".format(mock_stdout.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())

    def test_create_missing_class(self):
        correct = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("create"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())

    def test_create_invalid_class(self):
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("create MyModel"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())


class TestShowMethodWithAllErrors(unittest.TestCase):
    """"""
    def setUp(self):
        """Set up resources needed for the tests."""
        self.mock_stdout = StringIO()

    def tearDown(self):
        """Tear down resources after the tests."""
        self.mock_stdout.close()

    def test_show_no_instance_found_space_notationBaseModel(self):
        correct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("show BaseModel 1"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())

    def test_show_no_instance_found_space_notationUser(self):
        correct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("show User 1"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())

    def test_show_no_instance_found_space_notationState(self):
        correct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("show State 1"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())

    def test_show_no_instance_found_space_notationCity(self):
        correct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("show City 1"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())

    def test_show_no_instance_found_space_notationAmenity(self):
        correct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("show Amenity 1"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())

    def test_show_no_instance_found_space_notationPlace(self):
        correct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("show Place 1"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())

    def test_show_no_instance_found_space_notationReview(self):
        correct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("show Review 1"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())

    def test_show_no_instance_found_dot_notationBaseModel(self):
        correct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.show(123)"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())

    def test_show_no_instance_found_dot_notation_User(self):
        correct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("User.show(123)"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())

    def test_show_no_instance_found_dot_notation_State(self):
        correct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("State.show(123)"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())

    def test_show_no_instance_found_dot_notation_City(self):
        correct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("City.show(123)"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())

    def test_show_no_instance_found_dot_notation_Amenity(self):
        correct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("Amenity.show(123)"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())

    def test_show_no_instance_found_dot_notation_Place(self):
        correct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("Place.show(123)"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())

    def test_show_no_instance_found_dot_notation_Review(self):
        correct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("Review.show(123)"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())

    def test_show_no_instance_found_space_notationCity(self):
        correct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("show City 1"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())

    def test_do_show_missing_id_BaseModel(self):
        correct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("show BaseModel"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())

    def test_do_show_missing_id_User(self):
        correct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("show User"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())

    def test_do_show_missing_id_State(self):
        correct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("show State"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())

    def test_do_show_missing_id_City(self):
        correct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("show City"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())

    def test_do_show_missing_id_Amenity(self):
        correct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("show Amenity"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())

    def test_do_show_missing_id_Place(self):
        correct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("show Place"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())

    def test_do_show_missing_id_Review(self):
        correct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("show Review"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())

    def test_show_dot_missing_id_BaseModel(self):
        correct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.show()"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())

    def test_show_dot_missing_id_User(self):
        correct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("User.show()"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())

    def test_show_dot_missing_id_State(self):
        correct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("State.show()"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())

    def test_show_dot_missing_id_City(self):
        correct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("City.show()"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())

    def test_show_dot_missing_id_Amenity(self):
        correct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("Amenity.show()"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())

    def test_show_dot_missing_id_Place(self):
        correct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("Place.show()"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())

    def test_show_dot_missing_id_Review(self):
        correct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("Review.show()"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())

    def test_show_instance_BaseModel(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            testID = mock_stdout.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            obj = storage.all()["BaseModel.{}".format(testID)]
            command = "show BaseModel {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), mock_stdout.getvalue().strip())

    def test_show_instance_User(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            testID = mock_stdout.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            obj = storage.all()["User.{}".format(testID)]
            command = "show User {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), mock_stdout.getvalue().strip())

    def test_show_instance_State(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            testID = mock_stdout.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            obj = storage.all()["State.{}".format(testID)]
            command = "show State {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), mock_stdout.getvalue().strip())

    def test_show_instance_City(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            testID = mock_stdout.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            obj = storage.all()["Place.{}".format(testID)]
            command = "show Place {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), mock_stdout.getvalue().strip())

    def test_show_instance_Amenity(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            testID = mock_stdout.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            obj = storage.all()["City.{}".format(testID)]
            command = "show City {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), mock_stdout.getvalue().strip())

    def test_show_instance_Place(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            testID = mock_stdout.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            obj = storage.all()["Amenity.{}".format(testID)]
            command = "show Amenity {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), mock_stdout.getvalue().strip())

    def test_show_instance_Review(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            testID = mock_stdout.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            obj = storage.all()["Review.{}".format(testID)]
            command = "show Review {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), mock_stdout.getvalue().strip())

    def test_show_invalid_class(self):
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("show MyModel"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("MyModel.show()"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())


class TestDestroyMethod(unittest.TestCase):
    """"""

    def setUp(self):
        """Set up resources needed for the tests."""
        self.mock_stdout = StringIO()

    def tearDown(self):
        """Tear down resources after the tests."""
        self.mock_stdout.close()

    def test_destroy_space_invalid_class(self):
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("destroy MyModel"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())

    def test_destroy_dot_invalid_class(self):
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("MyModel.destroy()"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())

    def test_show_instance_No_Id(self):
        correct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            testID = mock_stdout.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            obj = storage.all()["Amenity.{}".format(testID)]
            command = "destroy Amenity"
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(correct, mock_stdout.getvalue().strip())

    def test_destroy_instance_success(self):
        correct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            testID = mock_stdout.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            obj = storage.all()["User.{}".format(testID)]
            command = "destroy Amenity {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(correct, mock_stdout.getvalue().strip())


class TestAllMethod(unittest.TestCase):
    """"""
    def setUp(self):
        """Set up resources needed for the tests."""
        self.mock_stdout = StringIO()

    def tearDown(self):
        """Tear down resources after the tests."""
        self.mock_stdout.close()

    def test_all_space_invalid_class(self):
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("all MyModel"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())

    def test_all_dot_invalid_class(self):
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("MyModel.all()"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())

    def test_all_objects_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("all"))
            self.assertIn("BaseModel", mock_stdout.getvalue().strip())
            self.assertIn("User", mock_stdout.getvalue().strip())
            self.assertIn("State", mock_stdout.getvalue().strip())
            self.assertIn("Place", mock_stdout.getvalue().strip())
            self.assertIn("City", mock_stdout.getvalue().strip())
            self.assertIn("Amenity", mock_stdout.getvalue().strip())
            self.assertIn("Review", mock_stdout.getvalue().strip())

    def test_all_single_object_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("all BaseModel"))
            self.assertIn("BaseModel", mock_stdout.getvalue().strip())
            self.assertNotIn("User", mock_stdout.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("all User"))
            self.assertIn("User", mock_stdout.getvalue().strip())
            self.assertNotIn("BaseModel", mock_stdout.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("all State"))
            self.assertIn("State", mock_stdout.getvalue().strip())
            self.assertNotIn("BaseModel", mock_stdout.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("all City"))
            self.assertIn("City", mock_stdout.getvalue().strip())
            self.assertNotIn("BaseModel", mock_stdout.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("all Amenity"))
            self.assertIn("Amenity", mock_stdout.getvalue().strip())
            self.assertNotIn("BaseModel", mock_stdout.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("all Place"))
            self.assertIn("Place", mock_stdout.getvalue().strip())
            self.assertNotIn("BaseModel", mock_stdout.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("all Review"))
            self.assertIn("Review", mock_stdout.getvalue().strip())
            self.assertNotIn("BaseModel", mock_stdout.getvalue().strip())

    def test_all_single_object_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.all()"))
            self.assertIn("BaseModel", mock_stdout.getvalue().strip())
            self.assertNotIn("User", mock_stdout.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("User.all()"))
            self.assertIn("User", mock_stdout.getvalue().strip())
            self.assertNotIn("BaseModel", mock_stdout.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("State.all()"))
            self.assertIn("State", mock_stdout.getvalue().strip())
            self.assertNotIn("BaseModel", mock_stdout.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("City.all()"))
            self.assertIn("City", mock_stdout.getvalue().strip())
            self.assertNotIn("BaseModel", mock_stdout.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("Amenity.all()"))
            self.assertIn("Amenity", mock_stdout.getvalue().strip())
            self.assertNotIn("BaseModel", mock_stdout.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("Place.all()"))
            self.assertIn("Place", mock_stdout.getvalue().strip())
            self.assertNotIn("BaseModel", mock_stdout.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("Review.all()"))
            self.assertIn("Review", mock_stdout.getvalue().strip())
            self.assertNotIn("BaseModel", mock_stdout.getvalue().strip())


class TestHBNBCommand_update(unittest.TestCase):
    """Unittests for testing update from the HBNB command interpreter."""
    def setUp(self):
        """Set up resources needed for the tests."""
        self.mock_stdout = StringIO()

    def tearDown(self):
        """Tear down resources after the tests."""
        self.mock_stdout.close()

    def test_update_invalid_class(self):
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("update MyModel"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("MyModel.update()"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())

    def test_update_missing_id_space_notation(self):
        correct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("update BaseModel"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("update User"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("update State"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("update City"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("update Amenity"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("update Place"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("update Review"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())

    def test_update_missing_id_dot_notation(self):
        correct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.update()"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("User.update()"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("State.update()"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("City.update()"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("Amenity.update()"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("Place.update()"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("Review.update()"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())

    def test_update_invalid_id_space_notation(self):
        correct = "** attribute name missing **"
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("update BaseModel 1"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("update User 1"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("update State 1"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("update City 1"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("update Amenity 1"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("update Place 1"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("update Review 1"))
            self.assertEqual(correct, mock_stdout.getvalue().strip())

    def test_update_missing_attr_name_space_notation(self):
        correct = "** attribute name missing **"
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            testId = mock_stdout.getvalue().strip()
            testCmd = "update BaseModel {}".format(testId)
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(correct, mock_stdout.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            testId = mock_stdout.getvalue().strip()
            testCmd = "update User {}".format(testId)
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(correct, mock_stdout.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            testId = mock_stdout.getvalue().strip()
            testCmd = "update State {}".format(testId)
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(correct, mock_stdout.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            testId = mock_stdout.getvalue().strip()
            testCmd = "update City {}".format(testId)
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(correct, mock_stdout.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            testId = mock_stdout.getvalue().strip()
            testCmd = "update Amenity {}".format(testId)
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(correct, mock_stdout.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            testId = mock_stdout.getvalue().strip()
            testCmd = "update Place {}".format(testId)
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(correct, mock_stdout.getvalue().strip())


if __name__ == '__main__':
    unittest.main()
