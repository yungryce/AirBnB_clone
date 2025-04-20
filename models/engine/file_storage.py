#!/usr/bin/python3
"""Module for FileStorage class."""

import json
import os
from models.base_model import BaseModel
# from models.user import User
# from models.state import State
# from models.city import City
# from models.amenity import Amenity
# from models.place import Place
# from models.review import Review


class FileStorage:
    """Serializes instances to a JSON file and
    Deserializes JSON file to instances"""

    __file_path = "file.json"
    __objects = {}
    __current_classes = {
        'BaseModel': BaseModel,
    #     'User': User,
    #     'State': State,
    #     'City': City,
    #     'Amenity': Amenity,
    #     'Place': Place,
    #     'Review': Review
    }

    def all(self):
        """return all objects stored in the file"""
        return self.__objects
        # return FileStorage.__objects

    def new(self, obj):
        """_summary_
        sets the object to the __objects dict and adds the key to the key

        Args:
            obj (_type_): dict of objects
        """
        if obj:
            key = f"{obj.__class__.__name__}.{obj.id}"
            self.__objects[key] = obj

    def save(self):
        """Serializes the objects to a JSON file"""
        serialized_obj = {}
        for key, value in self.__objects.items():
            serialized_obj[key] = value.to_dict()

        with open(self.__file_path, "w", encoding="UTF-8") as file:
            json.dump(serialized_obj, file)

    def reload(self):
        """Deserializes the JSON file to objects"""
        if os.path.exists(self.__file_path):
            try:
                with open(self.__file_path, "r") as file:
                    new_obj = json.load(file)
                    for key, val in new_obj.items():
                        # obj = BaseModel(**val)
                        # self.__objects[key] = obj
                        class_name = val['__class__']
                        if class_name in self.__current_classes:
                            class_obj = self.__current_classes[class_name]
                            obj = class_obj(**val)
                            self.__objects[key] = obj
            except Exception:
                pass
