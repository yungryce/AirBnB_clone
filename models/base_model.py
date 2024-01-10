#!/usr/bin/env python3
"""defines all common attributes/methods for other classes"""
from datetime import datetime
from uuid import uuid4
import models


class BaseModel:
    """defines all common attributes/methods for other classes"""
    def __init__(self, *args, **kwargs):
        """
        Initialize a class
        Args:
            *args: variable number of positional args in a tuple
            **kwargs (dict): Key/value pairs
        """
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if kwargs:
            for key, value in kwargs.items():
                if key in ["created_at", "updated_at"]:
                    setattr(self, key, datetime.fromisoformat(value))
                elif key not in ["__class__"]:
                    setattr(self, key, value)
        else:
            models.storage.new(self)

    def save(self):
        """updates public instance updated_at with the current datetime"""
        self.updated_at = datetime.now()
        models.storage.save()

    def __str__(self):
        """should print/str representation of the BaseModel instance."""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def to_dict(self):
        """returns a dictionary representation of the BaseModel instance
          using a shallow copy method"""
        obj_dict = self.__dict__.copy()
        for key, value in obj_dict.items():
            if isinstance(value, datetime):
                obj_dict[key] = value.isoformat()
        obj_dict["__class__"] = self.__class__.__name__
        # my_dict['updated_at'] = self.updated_at.isoformat()
        # my_dict['created_at'] = self.created_at.isoformat()
        return obj_dict
