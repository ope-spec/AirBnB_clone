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
        arg_list = arg.split('.')
        if arg == "" or arg == "all":
            obj_list = [str(obj) for obj in storage.all().values()]
        elif len(arg_list) == 1 and arg_list[0] in self.valid_classes:
            obj_list = [str(obj) for obj in storage.all().values() if isinstance(obj, self.valid_classes[arg_list[0]])]
        elif len(arg_list) == 2 and arg_list[1] == "all" and arg_list[0] in self.valid_classes:
            obj_list = [str(obj) for obj in storage.all().values() if isinstance(obj, self.valid_classes[arg_list[0]])]
        else:
            print("** class doesn't exist **")
            return

        print(obj_list)

    def do_update(self, arg):
        """
        Updates an instance based on the class name and id
        by adding or updating attributes (save the change into the JSON file).
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
                attribute_dict_str = args[2]
                attribute_dict = eval(attribute_dict_str)
                for attr_name, attr_value in attribute_dict.items():
                    if hasattr(instance, attr_name):
                        setattr(instance, attr_name, attr_value)
                    else:
                        print("** attribute doesn't exist **")
                        return
                instance.save()
            else:
                print("** no instance found **")

    def default(self, arg):
        """
        Default behavior for unrecognized commands.
        """
        if arg.endswith(".count()"):
            class_name = arg[:-8]  # Remove ".count()" from the command
            if class_name in self.valid_classes:
                count = sum(1 for obj in storage.all().values() if isinstance(obj, self.valid_classes[class_name]))
                print(count)
                return

        if arg.startswith("User.show"):
            args = arg.split("(")
            if len(args) == 2 and args[0] == "User.show" and args[1].endswith(")"):
                instance_id = args[1][1:-2].strip('\'"')
                instances = storage.all()
                for instance in instances.values():
                    if isinstance(instance, User) and instance.id == instance_id:
                        print(instance)
                        return
                print("** no instance found **")
                return

        if arg.startswith("User.update"):
            args = arg.split("(")
            if len(args) == 2 and args[0] == "User.update" and args[1].endswith(")"):
                params = args[1][1:-2].split(", ")
                instance_id = params[0].strip('\'"')
                attribute_dict_str = params[1]
                attribute_dict = eval(attribute_dict_str)
                instances = storage.all()
                for key, instance in instances.items():
                    class_name, obj_id = key.split('.')
                    if class_name == "User" and instance.id == instance_id:
                        for attr_name, attr_value in attribute_dict.items():
                            if hasattr(instance, attr_name):
                                setattr(instance, attr_name, attr_value)
                            else:
                                print("** attribute doesn't exist **")
                                return
                        instance.save()
                        return
                print("** no instance found **")
                return

        print("** Unknown command **")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
