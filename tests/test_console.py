import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand, validate_classname, validate_attrs
from console import count, current_classes


class TestHBNBCommand(unittest.TestCase):

    def setUp(self):
        self.mock_stdout = StringIO()

    def tearDown(self):
        self.mock_stdout.close()

    def assert_output(self, expected_output, function, *args):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            function(*args)
            self.assertEqual(mock_stdout.getvalue().strip(), expected_output)

    def test_quit_command(self):
        self.assert_output("", HBNBCommand().onecmd, "quit")

    def test_EOF_command(self):
        self.assert_output("", HBNBCommand().onecmd, "EOF")

    def test_emptyline_command(self):
        self.assert_output("", HBNBCommand().onecmd, "")

    def test_default_command(self):
        self.assert_output(
            "*** Unknown syntax: invalid_command\n"
            "*** Type help or? to list commands",
            HBNBCommand().onecmd,
            "invalid_command"
        )


class TestPreCmdMethod(unittest.TestCase):

    def setUp(self):
        self.mock_stdout = StringIO()

    def tearDown(self):
        self.mock_stdout.close()

    def test_precmd_empty_argument(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            result = HBNBCommand().precmd('')
        self.assertEqual('\n', result)
        self.assertEqual('', mock_stdout.getvalue())

    def test_precmd_invalid_command(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            result = HBNBCommand().precmd('invalid_command')
        self.assertEqual('invalid_command', result)
        self.assertEqual('', mock_stdout.getvalue())

    def test_precmd_valid_command_no_args(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            result = HBNBCommand().precmd('BaseModel.all()')
        self.assertEqual('all BaseModel', result)
        self.assertEqual('', mock_stdout.getvalue())

    def test_precmd_valid_command_with_args(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            result = HBNBCommand().precmd(
                'User.update("123", name, "John Doe")'
                )
        self.assertEqual('update User 123 name "John Doe"', result)
        self.assertEqual('', mock_stdout.getvalue())

    def test_precmd_invalid_class(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            result = HBNBCommand().precmd('InvalidClass.some_method()')
        self.assertEqual('\n', result)
        self.assertEqual('', mock_stdout.getvalue())

    def test_precmd_count_method(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            result = HBNBCommand().precmd('User.count()')
        self.assertEqual('\n', result)
        self.assertEqual('0\n', mock_stdout.getvalue())

    def test_precmd_invalid_count_method(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            result = HBNBCommand().precmd('InvalidClass.count()')
        self.assertEqual('count InvalidClass', result)
        self.assertEqual('', mock_stdout.getvalue())

    def test_precmd_invalid_args_format(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            result = HBNBCommand().precmd(
                'User.update("123", name, "John Doe", invalid_arg)'
                )
        self.assertEqual('update User 123 name "John Doe"', result)
        self.assertEqual(
            '*** Unknown syntax: '
            'User.update("123", name, "John Doe", invalid_arg)\n***'
            'Type help or? to list commands\n',
            mock_stdout.getvalue()
            )

    def test_precmd_edge_case_empty_string(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            result = HBNBCommand().precmd('""')
        self.assertEqual('""', result)
        self.assertEqual('', mock_stdout.getvalue())

    def test_precmd_edge_case_invalid_syntax(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            result = HBNBCommand().precmd('User.update(,)')
        self.assertEqual('update User', result)
        self.assertEqual(
            '*** Unknown syntax: User.update(,)\n*** '
            'Type help or? to list commands\n', mock_stdout.getvalue()
            )

    def test_precmd_edge_case_invalid_method(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            result = HBNBCommand().precmd('User.invalid_method()')
        self.assertEqual('invalid_method User', result)
        print("++++++++++++++", mock_stdout.getvalue(), "++++++++++++++")
        self.assertEqual(
            '*** Unknown syntax: invalid_method User\n'
            '*** Type help or? to list commands\n',
            mock_stdout.getvalue()
            )


if __name__ == '__main__':
    unittest.main()
