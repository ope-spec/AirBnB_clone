#!/usr/bin/python3
"""
Module: console
Entry point for the HBNB command interpreter.
"""

import cmd
import json
from models.base_model import BaseModel
from models import storage


class HBNBCommand(cmd.Cmd):
    """
    HBNBCommand class.
    Entry point for the HBNB command interpreter.
    """

    prompt = '(hbnb) '

    def do_quit(self, arg):
        """
        Exit the program.
        """
        return True

    def do_EOF(self, arg):
        """
        Exit the program.
        """
        return True

    def emptyline(self):
        """
        Do nothing on empty line.
        """
        pass

    def do_create(self, arg):
        """
        Creates a new instance of BaseModel, saves it (to the JSON file)
        and prints the id.
        Usage: create <class name>
        """
        if not arg:
            print('** class name missing **')
            return

        class_name = arg.strip()
        if class_name not in storage.classes:
            print('** class doesn\'t exist **')
            return

        new_instance = storage.classes[class_name]()
        new_instance.save()
        print(new_instance.id)

    def do_show(self, arg):
        """
        Prints the string representation of an instance
        based on the class name and id.
        Usage: show <class name> <id>
        """
        if not arg:
            print('** class name missing **')
            return

        args = arg.split()
        class_name = args[0]
        if class_name not in storage.classes:
            print('** class doesn\'t exist **')
            return

        if len(args) < 2:
            print('** instance id missing **')
            return

        obj_id = args[1]
        key = '{}.{}'.format(class_name, obj_id)
        if key not in storage.all():
            print('** no instance found **')
            return

        print(storage.all()[key])

    def do_destroy(self, arg):
        """
        Deletes an instance based on the class name and id
        (save the change into the JSON file).
        Usage: destroy <class name> <id>
        """
        if not arg:
            print('** class name missing **')
            return

        args = arg.split()
        class_name = args[0]
        if class_name not in storage.classes:
            print('** class doesn\'t exist **')
            return

        if len(args) < 2:
            print('** instance id missing **')
            return

        obj_id = args[1]
        key = '{}.{}'.format(class_name, obj_id)
        if key not in storage.all():
            print('** no instance found **')
            return

        storage.all().pop(key)
        storage.save()

    def do_all(self, arg):
        """
        Prints all string representation of all instances
        based or not on the class name.
        Usage: all or all <class name>
        """
        args = arg.split()
        if not arg:
            print([str(obj) for obj in storage.all().values()])
            return

        class_name = args[0]
        if class_name not in storage.classes:
            print('** class doesn\'t exist **')
            return

        print([str(obj) for obj in storage.all().values()
               if obj.__class__.__name__ == class_name])

    def do_update(self, arg):
        """
        Updates an instance based on the class name and id
        by adding or updating attribute (save the change into the JSON file).
        Usage: update <class name> <id> <attribute name> "<attribute value>"
        """
        if not arg:
            print('** class name missing **')
            return

        args = arg.split()
        class_name = args[0]
        if class_name not in storage.classes:
            print('** class doesn\'t exist **')
            return

        if len(args) < 2:
            print('** instance id missing **')
            return

        obj_id = args[1]
        key = '{}.{}'.format(class_name, obj_id)
        if key not in storage.all():
            print('** no instance found **')
            return

        if len(args) < 3:
            print('** attribute name missing **')
            return

        if len(args) < 4:
            print('** value missing **')
            return

        attribute_name = args[2]
        attribute_value = args[3].strip('"')

        instance = storage.all()[key]
        setattr(instance, attribute_name, attribute_value)
        instance.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
