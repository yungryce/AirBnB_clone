#!/usr/bin/python3
""""""
import cmd
import shlex
from models import storage
from models.base_model import BaseModel

current_classes = {
    'BaseModel': BaseModel,
}


class HBNBCommand(cmd.Cmd):
    """
    Command interpreter for HBNB project
    any command that returns a true value stops the interpreter.
    """

    prompt = "(hbnb) "

    """def do_help(self, arg):
        # To get help on a command, type help <topic>.
        return super().do_help(arg)"""

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

    def default(self, line):
        """
        Default method to be called when none of the above commands match
        """
        print(f"*** Unknown syntax: {line}")
        print(f"*** Type help or? to list commands")

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
        l = []
        if not args:
            for key in storage.all():
                l.append(str(storage.all()[key]))
        elif args[0] not in current_classes.keys():
            print("** class doesn't exist **")
        else:
            for key in storage.all():
                if key.startswith(args[0]):
                    l.append(str(storage.all()[key]))
                    
        print(l)

    def do_update(self, arg):
        """
        Updates an instance based on user input
        Usage:  update <class name> <id> <attribute name> "<attribute value>"
        """
        args = shlex.split(arg)
        
        if (not validate_classname(args, check_id=True)
            or not validate_attrs(args)):
            return
        key = f"{args[0]}.{args[1]}"
        if key in storage.all():
            instance = storage.all()[key].to_dict()
            if args[2] in instance.keys():
                type_value = type(instance[args[2]])
                instance[args[2]] = type_value(args[3])
            else:
                instance[args[2]] = args[3].strip('"')
        else:
            print("** no instance found **")
            
        new_instance = current_classes[args[0]](**instance)
        storage.new(new_instance)
        new_instance.save()

    def do_type(self, arg):
        """
        checks the types of attributes in an instance
        Usage:  checkTypes <class name> <id> <attribute name>
        """
        args = shlex.split(arg)
        if not validate_classname(args, check_id=True):
            return
        if not args[2]:
            print("** attribute name missing **")
            return
        key = f"{args[0]}.{args[1]}"
        if key in storage.all():
            for key, value in storage.all()[key].to_dict().items():
                print(f"{key}: {type(value)}")

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
    """Runs checks on args to validate classname attributes and values.
    """
    if len(args) < 3:
        print("** attribute name missing **")
        return False
    if len(args) < 4:
        print("** value missing **")
        return False
    return True


if __name__ == '__main__':
    HBNBCommand().cmdloop()
