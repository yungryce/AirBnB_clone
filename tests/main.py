#!/usr/bin/python3
""" Test File """
import sys
sys.path.append("..")
from models.base_model import BaseModel
from models import storage
from uuid import uuid4

if __name__ == "__main__":
    all_objs = storage.all()
    print("-- Reloaded objects --")
    for obj_id in all_objs.keys():
        obj = all_objs[obj_id]
        print(obj)

    print("-- Create a new object --")
    my_model = BaseModel()
    my_model.name = "My First Model"
    my_model.my_number = 89    
    my_model.save()
    print(my_model)
    # print(str(my_model))
    # print(my_model.__str__())
    
    print()
    print("----")
    print()

    print(f"Basemodel: {type(my_model)}")
    print(f"Object ID: {type(my_model.id)} {my_model.id}")
    print(f"Created at: {type(my_model.created_at)} {my_model.created_at}")

    print()
    print("----")
    print()

    my_model_json = my_model.to_dict()
    print(type(my_model_json))
    print(my_model_json)
    print("JSON of my_model:")
    for key in my_model_json.keys():
        print("\t{}: ({}) - {}".format(key, type(my_model_json[key]), my_model_json[key]))

    print()
    print("----")
    print()

    my_new_model = BaseModel(**my_model_json)
    print(my_new_model.id)
    print(my_new_model)
    print(type(my_new_model.created_at))
    print(type(my_new_model))
    print(my_model is my_new_model)
    print(my_model == my_new_model)
    
    print()
    print("----")
    print()
    
    new_uuid = str(uuid4())
    new_model = BaseModel(id=new_uuid, name="My third Model", my_number=9)
    print(new_model.name)
    print("--")
