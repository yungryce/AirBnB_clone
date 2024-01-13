    def test_precmd_edge_case_invalid_count_syntax(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            result = HBNBCommand().precmd('User.count(')
        self.assertEqual('User.count(', result)
        self.assertEqual(
            '*** Unknown syntax: User.count(\n*** '
            'Type help or? to list commands\n',
            mock_stdout.getvalue()
            )


class TestCreateCommand(unittest.TestCase):

    def setUp(self):
        self.mock_stdout = StringIO()

    def tearDown(self):
        self.mock_stdout.close()

    def assert_output(self, expected_output, function, *args):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            function(*args)
            self.assertEqual(mock_stdout.getvalue().strip(), expected_output)

    def test_create_command(self):
        with patch('models.storage', autospec=True) as mock_storage:
            self.assert_output("0000-0000-0000-0000", HBNBCommand().do_create, "BaseModel")
            mock_storage.save.assert_called_once()

    def test_create_command_invalid_class(self):
        self.assert_output("** class doesn't exist **", HBNBCommand().do_create, "InvalidClass")

    def test_create_command_missing_classname(self):
        self.assert_output("** class name missing **", HBNBCommand().do_create, "")

    def test_create_command_invalid_id(self):
        self.assert_output("** instance id missing **", HBNBCommand().do_create, "BaseModel")


class TestShowCommand(unittest.TestCase):
    def test_show_command(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            HBNBCommand().do_create("BaseModel")
            instance_id = mock_stdout.getvalue().strip()

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.assert_output(str(current_classes["BaseModel"](id=instance_id)), HBNBCommand().do_show, "BaseModel", instance_id)

    def test_show_command_no_instance(self):
        self.assert_output("** no instance found **", HBNBCommand().do_show, "BaseModel", "invalid_id")

    def test_show_command_no_class_name(self):
        self.assert_output("** class name missing **", HBNBCommand().do_show, "", "some_id")

    def test_show_command_no_instance_id(self):
        self.assert_output("** instance id missing **", HBNBCommand().do_show, "BaseModel", "")

    def test_show_command_invalid_class(self):
        self.assert_output("** class doesn't exist **", HBNBCommand().do_show, "InvalidClass", "some_id")

class TestDestroyCommand(unittest.TestCase):
    def test_destroy_command(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            HBNBCommand().do_create("BaseModel")
            instance_id = mock_stdout.getvalue().strip()

        with patch('models.storage', autospec=True) as mock_storage, \
             patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.assert_output("", HBNBCommand().do_destroy, "BaseModel", instance_id)
            mock_storage.save.assert_called_once()
            self.assertNotIn(f"BaseModel.{instance_id}", mock_storage.all())

    def test_destroy_command_no_instance(self):
        self.assert_output("** no instance found **", HBNBCommand().do_destroy, "BaseModel", "invalid_id")
    def test_destroy_command_no_class_name(self):
        self.assert_output("** class name missing **", HBNBCommand().do_destroy, "", "some_id")
    def test_destroy_command_no_instance_id(self):
        self.assert_output("** instance id missing **", HBNBCommand().do_destroy, "BaseModel", "")
    def test_destroy_command_invalid_class(self):
        self.assert_output("** class doesn't exist **", HBNBCommand().do_destroy, "InvalidClass", "some_id")
    def test_destroy_command_invalid_instance(self):
        self.assert_output("** no instance found **", HBNBCommand().do_destroy, "BaseModel", "invalid_id")
    def test_destroy_command_mismatch_class_instance(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            HBNBCommand().do_create("BaseModel")
            instance_id = mock_stdout.getvalue().strip()

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.assert_output("** no instance found **", HBNBCommand().do_destroy, "InvalidClass", instance_id)

class TestAllCommand(unittest.TestCase):
    def test_all_command_no_class_name(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            HBNBCommand().do_all("")
        self.assertEqual("[]\n", mock_stdout.getvalue())
    def test_all_command_with_class_name(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            HBNBCommand().do_all("BaseModel")
        self.assertIn("BaseModel", mock_stdout.getvalue())
    def test_all_command_invalid_class(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            HBNBCommand().do_all("InvalidClass")
        self.assertEqual("** class doesn't exist **\n", mock_stdout.getvalue())
    def test_all_command_no_instances(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            HBNBCommand().do_all("BaseModel")
        self.assertEqual("[]\n", mock_stdout.getvalue())
    def test_all_command_invalid_class_no_instances(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            HBNBCommand().do_all("InvalidClass")
        self.assertEqual("** class doesn't exist **\n", mock_stdout.getvalue())

class TestUpdateCommand(unittest.TestCase):
    def test_update_command_incomplete_args(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            HBNBCommand().do_update("BaseModel some_id")
        self.assertEqual("** attribute name missing **\n", mock_stdout.getvalue())
    def test_update_command_invalid_class(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            HBNBCommand().do_update("InvalidClass some_id attr_name value")
        self.assertEqual("** class doesn't exist **\n", mock_stdout.getvalue())
    def test_update_command_invalid_instance(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            HBNBCommand().do_update("BaseModel invalid_id attr_name value")
        self.assertEqual("** no instance found **\n", mock_stdout.getvalue())
    def test_update_command_valid_args(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            HBNBCommand().do_create("BaseModel")
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            HBNBCommand().do_update("BaseModel some_id name 'New Name'")
        self.assertIn("'name': 'New Name'", mock_stdout.getvalue())
    def test_update_command_incomplete_args(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            HBNBCommand().do_update("BaseModel some_id")
        self.assertEqual("** attribute name missing **\n", mock_stdout.getvalue())
    def test_update_command_invalid_class(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            HBNBCommand().do_update("InvalidClass some_id attr_name value")
        self.assertEqual("** class doesn't exist **\n", mock_stdout.getvalue())
    def test_update_command_invalid_instance_id(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            HBNBCommand().do_update("BaseModel invalid_id attr_name value")
        self.assertEqual("** no instance found **\n", mock_stdout.getvalue())
    def test_update_command_invalid_attr_type(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            HBNBCommand().do_create("BaseModel")
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            HBNBCommand().do_update("BaseModel some_id name 42")
        self.assertEqual("** value must be a string **\n", mock_stdout.getvalue())
    def test_update_command_numeric_value(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            HBNBCommand().do_create("BaseModel")
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            HBNBCommand().do_update("BaseModel some_id age 42")
        self.assertIn("'age': 42", mock_stdout.getvalue())

class TestSupportFunctions(unittest.TestCase):

    def test_count_valid_class(self):
        with unittest.mock.patch('models.storage.all', return_value={'BaseModel.1': {}, 'BaseModel.2': {}}):
            result = count('BaseModel')
        self.assertEqual(result, 2)

    def test_count_invalid_class(self):
        with unittest.mock.patch('models.storage.all', return_value={'InvalidClass.1': {}, 'InvalidClass.2': {}}):
            result = count('BaseModel')
        self.assertEqual(result, 0)

    def test_validate_classname(self):
        self.assertTrue(validate_classname(["BaseModel"]))
        self.assertFalse(validate_classname([], True))
        self.assertFalse(validate_classname(["InvalidClass"]))
        self.assertTrue(validate_classname(["BaseModel", "123"], True))
        self.assertFalse(validate_classname(["BaseModel"], True))

    def test_validate_classname_valid(self):
        args = ['BaseModel', '1']
        result = validate_classname(args, check_id=True)
        self.assertTrue(result)

    def test_validate_classname_missing_classname(self):
        args = []
        result = validate_classname(args)
        self.assertFalse(result)
        self.assertEqual(self.mock_stdout.getvalue().strip(), '** class name missing **')

    def test_validate_classname_invalid_class(self):
        args = ['InvalidClass']
        result = validate_classname(args)
        self.assertFalse(result)
        self.assertEqual(self.mock_stdout.getvalue().strip(), '** class doesn\'t exist **')

    def test_validate_classname_missing_id(self):
        args = ['BaseModel']
        result = validate_classname(args, check_id=True)
        self.assertFalse(result)
        self.assertEqual(self.mock_stdout.getvalue().strip(), '** instance id missing **')

    def test_validate_attrs_valid(self):
        args = ['BaseModel', '1', 'attribute_name', 'value']
        result = validate_attrs(args)
        self.assertTrue(result)

    def test_validate_attrs_missing_name(self):
        args = ['BaseModel', '1', '']
        result = validate_attrs(args)
        self.assertFalse(result)
        self.assertEqual(self.mock_stdout.getvalue().strip(), '** attribute name missing **')

    def test_validate_attrs_missing_value(self):
        args = ['BaseModel', '1', 'attribute_name']
        result = validate_attrs(args)
        self.assertFalse(result)
        self.assertEqual(self.mock_stdout.getvalue().strip(), '** value missing **')

    def test_count_valid_class(self):
        with unittest.mock.patch('models.storage.all', return_value={'BaseModel.1': {}, 'BaseModel.2': {}}):
            result = count('BaseModel')
        self.assertEqual(result, 2)

    def test_count_invalid_class(self):
        with unittest.mock.patch('models.storage.all', return_value={'InvalidClass.1': {}, 'InvalidClass.2': {}}):
            result = count('BaseModel')
        self.assertEqual(result, 0)

    def test_count_no_instances(self):
        with unittest.mock.patch('models.storage.all', return_value={}):
            result = count('BaseModel')
        self.assertEqual(result, 0)

    def test_validate_classname_valid(self):
        args = ['BaseModel', '1']
        result = validate_classname(args, check_id=True)
        self.assertTrue(result)

    def test_validate_classname_missing_classname(self):
        args = []
        result = validate_classname(args)
        self.assertFalse(result)
        self.assertEqual(self.mock_stdout.getvalue().strip(), '** class name missing **')

    def test_validate_classname_invalid_class(self):
        args = ['InvalidClass']
        result = validate_classname(args)
        self.assertFalse(result)
        self.assertEqual(self.mock_stdout.getvalue().strip(), '** class doesn\'t exist **')

    def test_validate_classname_missing_id(self):
        args = ['BaseModel']
        result = validate_classname(args, check_id=True)
        self.assertFalse(result)
        self.assertEqual(self.mock_stdout.getvalue().strip(), '** instance id missing **')

    def test_validate_attrs_valid(self):
        args = ['BaseModel', '1', 'attribute_name', 'value']
        result = validate_attrs(args)
        self.assertTrue(result)

    def test_validate_attrs_missing_name(self):
        args = ['BaseModel', '1', '']
        result = validate_attrs(args)
        self.assertFalse(result)
        self.assertEqual(self.mock_stdout.getvalue().strip(), '** attribute name missing **')

    def test_validate_attrs_missing_value(self):
        args = ['BaseModel', '1', 'attribute_name']
        result = validate_attrs(args)
        self.assertFalse(result)
        self.assertEqual(self.mock_stdout.getvalue().strip(), '** value missing **')

    def test_validate_attrs_none_value(self):
        args = ['BaseModel', '1', 'attribute_name', 'None']
        result = validate_attrs(args)
        self.assertTrue(result)

    def test_validate_attrs_none_name(self):
        args = ['BaseModel', '1', 'None', 'value']
        result = validate_attrs(args)
        self.assertTrue(result)

    def test_validate_attrs_none_name_and_value(self):
        args = ['BaseModel', '1', 'None', 'None']
        result = validate_attrs(args)
        self.assertTrue(result)

    def test_default_command(self):
        self.assert_output("*** Unknown syntax: invalid_command", HBNBCommand().default, "invalid_command")

    def test_unknown_syntax_command(self):
        self.assert_output("*** Unknown syntax: invalid_command", HBNBCommand().default, "invalid_command")

    def test_unknown_syntax_command_empty(self):
        self.assert_output("*** Unknown syntax: ", HBNBCommand().default, "")