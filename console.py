#!/usr/bin/python3
""""""
import cmd
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
        """Creates a new instance of BaseModel"""
        args = arg.split()
        if not validate_classname(args):
            return
        new_instance = current_classes[args[0]]()
        new_instance.save()
        print(new_instance.id)
        
    
    def do_show(self, arg):
        """Prints the string representation of an instance"""
        args = arg.split()
        if not validate_classname(args, check_id=True):
            return
        key = f"{args[0]}.{args[1]}"
        if key in storage.all():
            print(storage.all()[key])
        else:
            print("** no instance found **")
    
    def do_destroy(self, arg):
        """Deletes an instance from the storage"""
        args = arg.split()
        if not validate_classname(args, check_id=True):
            return
        key = f"{args[0]}.{args[1]}"
        if key in storage.all():
            del(storage.all()[key])
            storage.save()
        else:
            print("** no instance found **")
    
    def do_all(self, arg):
        """Prints all string representations of all instances"""
        args = arg.split()
        if not args:
            for key in storage.all():
                print(storage.all()[key])
        elif args[0] not in current_classes.keys():
                print("** class doesn't exist **")
        else:
            for key in storage.all():
                if key.startswith(args[0]):
                    print(storage.all()[key])


    def do_update(self, arg):
        """Updates an instance based on user input"""
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