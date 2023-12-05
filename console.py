#!/usr/bin/python3
"""Entry point of the command interpreter"""


import cmd
import models


class HBNBCommand(cmd.Cmd):
    """Console class"""
    prompt = "(hbnb) "

    def do_quit(self, line):
        """Command to exit the interpreter"""
        return True

    do_EOF = do_quit

    def emptyline(self):
        pass

if __name__ == '__main__':
    HBNBCommand().cmdloop()
