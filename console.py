#!/usr/bin/python3
"""This module defines the HBNBCommand class, a command interpreter."""

import cmd
from models.base_model import BaseModel
import models


class HBNBCommand(cmd.Cmd):
    """Command interpreter for the HBNB project."""

    prompt = "(hbnb) "
    valid_classes = {
        "BaseModel": BaseModel
        # Add more class mappings here if needed
    }

    def do_quit(self, arg):
        """Exit the program."""
        return True

    def do_EOF(self, arg):
        """Exit the program."""
        return True

    def emptyline(self):
        """Do nothing when an empty line is entered."""
        pass

    def do_create(self, arg):
        """Create a new instance of BaseModel, save it, and print the id."""
        if not arg:
            print("** class name missing **")
        elif arg not in self.valid_classes:
            print("** class doesn't exist **")
        else:
            new_instance = self.valid_classes[arg]()
            new_instance.save()
            print(new_instance.id)

    def do_show(self, arg):
        """Print the string representation of an instance."""
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            instances = models.storage.all()
            instance_key = args[0] + "." + args[1]
            if instance_key in instances:
                print(instances[instance_key])
            else:
                print("** no instance found **")

    def do_destroy(self, arg):
        """Delete an instance based on the class name and id."""
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            instances = models.storage.all()
            instance_key = args[0] + "." + args[1]
            if instance_key in instances:
                del instances[instance_key]
                models.storage.save()
            else:
                print("** no instance found **")

    def do_all(self, arg):
        """Print all string representations of instances."""
        instances = models.storage.all()
        if not arg:
            print([str(instance) for instance in instances.values()])
        elif arg in self.valid_classes:
            class_name = self.valid_classes[arg].__name__
            print([str(instance) for instance in instances.values()
                   if instance.__class__.__name__ == class_name])
        else:
            print("** class doesn't exist **")

    def do_update(self, arg):
        """Update an instance based on the class name and id."""
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        elif len(args) < 3:
            print("** attribute name missing **")
        elif len(args) < 4:
            print("** value missing **")
        else:
            instances = models.storage.all()
            instance_key = args[0] + "." + args[1]
            if instance_key in instances:
                instance = instances[instance_key]
                attribute_name = args[2]
                attribute_value = args[3]
                setattr(instance, attribute_name, attribute_value)
                instance.save()
            else:
                print("** no instance found **")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
