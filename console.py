#!/usr/bin/python3
"""
Module: console
Entry point for the HBNB command interpreter.
"""

import cmd
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage


class HBNBCommand(cmd.Cmd):
    """
    HBNBCommand class.
    Entry point for the HBNB command interpreter.
    """

    prompt = "(hbnb) "
    valid_classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
    }

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
        Creates a new instance of BaseModel or User,
        saves it (to the JSON file) and prints the id.
        Usage: create <class name>
        """
        if not arg:
            print("** class name missing **")
        elif arg not in self.valid_classes:
            print("** class doesn't exist **")
        else:
            new_instance = self.valid_classes[arg]()
            new_instance.save()
            print(new_instance.id)

    def do_show(self, arg):
        """
        Prints the string representation of an instance
        based on the class name and id.
        Usage: show <class name> <id>
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            instances = storage.all()
            instance_key = args[0] + "." + args[1]
            if instance_key in instances:
                print(instances[instance_key])
            else:
                print("** no instance found **")

    def do_destroy(self, arg):
        """
        Deletes an instance based on the class name and id
        (save the change into the JSON file).
        Usage: destroy <class name> <id>
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            instances = storage.all()
            instance_key = args[0] + "." + args[1]
            if instance_key in instances:
                del instances[instance_key]
                storage.save()
            else:
                print("** no instance found **")

    def do_all(self, arg):
        """
        Prints all string representation of all instances
        based or not on the class name.
        Usage: all or all <class name>
        """
        instances = storage.all()
        if not arg:
            print([str(instance) for instance in instances.values()])
        elif arg in self.valid_classes:
            class_instances = [
                str(instance)
                for instance in instances.values()
                if isinstance(instance, self.valid_classes[arg])
            ]
            print(class_instances)
        else:
            print("** class doesn't exist **")

    def do_update(self, arg):
        """
        Updates an instance based on the class name and id
        by adding or updating attribute (save the change into the JSON file).
        Usage: update <class name> <id> <attribute name> "<attribute value>"
        """
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
            instances = storage.all()
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
