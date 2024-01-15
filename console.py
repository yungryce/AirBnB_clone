#!/usr/bin/python3
"""
Command line interface module.
Prompt:
    (hbnb)
Commands:
    help - displays a list of commands
    quit - exits the program
    create - creates a new instance of a class
    show - displays an instance of a class
    all - displays all instances of a class
    destroy - destroys an instance of a class
    update - updates an instance of a class
"""
import cmd
import re
import shlex
import ast
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


current_classes = {
    'BaseModel': BaseModel,
    'User': User,
    'State': State,
    'City': City,
    'Amenity': Amenity,
    'Place': Place,
    'Review': Review
}


class HBNBCommand(cmd.Cmd):
    """
    Command interpreter for HBNB project
    Any command that returns a true value stops the interpreter.
    """

    prompt = "(hbnb) "

    def precmd(self, arg):
        """
        Pre-process the command line before it is interpreted.
        Usage:
            <Class Name>.<method name>(arg1, arg2, arg3)
        """
        if not arg or arg == '':
            return '\n'

        pattern = re.compile(r'(\w+)\.(\w+)\((.*)\)')
        tuple_match = pattern.findall(arg)
        if not tuple_match:
            return super().precmd(arg)

        match_list = tuple_match[0]
        if not match_list[1] or not hasattr(self, 'do_' + match_list[1]):
            return '\n'

        all_args = [match_list[1], match_list[0]]
        if len(match_list) > 2 and match_list[2] != '':
            dict_pattern = re.compile(r'\{.+?\}')
            dict_match = dict_pattern.search(match_list[2])
            if dict_match:
                uuid_pattern = re.compile(r'"([^"]*)"')
                uuid_match = uuid_pattern.search(match_list[2])
                if uuid_match:
                    all_args.append(uuid_match.group(1))
                    all_args.append(dict_match.group(0))
            else:
                args = [arg.rstrip(',') for arg in shlex.split(match_list[2])]
                all_args.extend(args)

        if len(all_args) > 4 and ' ' in all_args[4]:
            args[2] = args[2].replace(' ', '_')

        args_str = ' '.join(all_args[1:])
        method_name = 'do_' + all_args[0]
        getattr(self, method_name)(args_str)
        return '\n'

    def default(self, arg):
        """Default method for unknown commands"""
        self.precmd(arg)

    def do_count(self, arg):
        """Returns count of all Instances of a class"""
        args = shlex.split(arg)
        intance = storage.all()
        print(len([x for x in intance if x.startswith(args[0])]))

    def do_create(self, arg):
        """
        Creates a new instance of BaseModel
        Usage:  create <class name>
        """
        args = shlex.split(arg)
        if not validate_classname(args):
            return
        new_instance = current_classes[args[0]]()
        new_instance.save()
        print(new_instance.id)

    def do_show(self, arg):
        """
        Prints the string representation of an instance
        Usage:  show <class name> <id>
        """
        args = shlex.split(arg)
        if not validate_classname(args, check_id=True):
            return
        key = f"{args[0]}.{args[1]}"
        if key in storage.all():
            print(storage.all()[key])
        else:
            print("** no instance found **")

    def do_destroy(self, arg):
        """
        Deletes an instance from the storage
        Usage:  destroy <class name> <id>
        """
        args = shlex.split(arg)
        if not validate_classname(args, check_id=True):
            return
        key = f"{args[0]}.{args[1]}"
        if key in storage.all():
            del (storage.all()[key])
            storage.save()
        else:
            print("** no instance found **")

    def do_all(self, arg):
        """
        Prints all string representations of all instances
        Usage:  all
                all <class name>
        """
        args = shlex.split(arg)
        str_list = []
        if not args:
            for key in storage.all():
                str_list.append(str(storage.all()[key]))
        elif validate_classname(args):
            for key in storage.all():
                if key.startswith(args[0]):
                    str_list.append(str(storage.all()[key]))
        if str_list:
            print(str_list)

    def do_update(self, arg):
        """
        Updates an instance based on user input
        Usage:  update <class name> <id> <attribute name> "<attribute value>"
        """
        pattern = re.compile(r'\{.*?\}')
        dict_match = pattern.search(arg)

        if dict_match:
            new_pattern = re.compile(r'(\w+)\s+(\S+).*')
            new_match = new_pattern.search(arg)
            if new_match:
                base_args = [new_match.group(1), new_match.group(2)]

            str_dict = ast.literal_eval(dict_match.group())
            for key, value in str_dict.items():
                updated_args = base_args.copy()
                updated_args.append(key)
                updated_args.append(str(value))
                if updated_args[3] and ' ' in updated_args[3]:
                    updated_args[3] = updated_args[3].replace(' ', '_')
                updated_arg = ', '.join(updated_args)
                self.do_update(updated_arg)
            return
        else:
            args = [arg.rstrip(',') for arg in shlex.split(arg)]

        if (not validate_classname(args, check_id=True)
                or not validate_attrs(args)):
            return

        if args[3] and '_' in args[3]:
            args[3] = args[3].replace('_', ' ')

        key = f"{args[0]}.{args[1]}"
        if key in storage.all():
            instance = storage.all()[key].to_dict()
            if args[2] in instance.keys():
                type_value = type(instance[args[2]])
                instance[args[2]] = type_value(args[3])
            else:
                instance[args[2]] = args[3]
        else:
            print("** no instance found **")
            return False

        new_instance = current_classes[args[0]](**instance)
        storage.new(new_instance)
        new_instance.save()

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """Exit the program"""
        print()  # Add a new line before exiting
        return True

    def emptyline(self):
        """Do nothing on empty line"""
        pass


def validate_classname(args, check_id=False):
    """Runs checks on args to validate classname entry.
    """
    if len(args) < 1:
        print("** class name missing **")
        return False
    if args[0] not in current_classes.keys():
        print("** class doesn't exist **")
        return False
    if len(args) < 2 and check_id:
        print("** instance id missing **")
        return False
    return True


def validate_attrs(args):
    """Runs checks on args to validate classname attributes and values."""
    if len(args) < 3:
        print("** attribute name missing **")
        return False
    if len(args) < 4:
        print("** value missing **")
        return False
    return True


if __name__ == '__main__':
    HBNBCommand().cmdloop()
