if len(args) == 1:
    return f"{match_tuple[1]} {match_tuple[0]} {args[0]}"
elif len(args) == 2:
    return f"{match_tuple[1]} {match_tuple[0]} {args[0]} {args[1]}"
elif len(args) > 2:
    return f"{match_tuple[1]} {match_tuple[0]} {args[0]} {args[1]} {args[2]}"



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



def do_help(self, arg):
    """To get help on a command, type help <topic>."""
    return super().do_help(arg)"""



def precmd(self, arg):
    """
    Pre-process the command line before it is interpreted.
    Usage:
        <Class Name>.<method name>(arg1, arg2, arg3)
    """
    if not arg:
        return '\n'

    pattern = re.compile(r'(\w+)\.(\w+)\((.*)\)')
    pattern_match = pattern.findall(arg)
    if not pattern_match:
        return super().precmd(arg)

    if match_tuple[2]:
        args = [arg.strip(',') for arg in shlex.split(match_tuple[2])]
        match_tuple.extends(args)

    if not self.is_valid_method(match_tuple[1]):
    
    match_tuple = pattern_match[0]
    if not match_tuple[0] in current_classes or not self.is_valid_method(match_tuple[1]):
        return "\n"
    elif not match_tuple[2]:
        if match_tuple[1] == "count":
            print(count(match_tuple[0]))
            return "\n"
        else:
            return f"{match_tuple[1]} {match_tuple[0]}"
    else:
        args = [arg.strip(',') for arg in shlex.split(match_tuple[2])]
        if not args[1]:
            if match_tuple[1] == "all":
                return f"{match_tuple[1]} {match_tuple[0]} {args[0]}"
            elif
        if len(args) > 2:
            args[2] = args[2].replace(' ', '_')
        args.extend([None] * (3 - len(args)))
        return (
            f"{match_tuple[1]} {match_tuple[0]} {args[0]} "
            f"{args[1]} {args[2]}"
        )


def default(self, arg):
    """
    Default method to be called when none of the above commands match
    """
    print(f"*** Unknown syntax: {arg}")
    print(f"*** Type help or? to list commands")