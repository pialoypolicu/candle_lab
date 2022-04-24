from django.db import transaction
from pprint import pprint
from core_storage.models import Purchase, ArrivalWait


def create_position_in_purchase(data):
    try:
         created_object = Purchase.objects.create(**data)
    except TypeError as error:
        print("Error in create_position", error)
        return False
    return created_object


def create_or_update_arrival_wait(data):
    del data['date_purchase']
    del data['price']
    name = data['name']
    exist_object_in_arrival = ArrivalWait.objects.filter(name=name).exists()
    if exist_object_in_arrival:
        quantity = data['quantity']
        weight = data['weight']
        arrival_object = ArrivalWait.objects.get(name=name)
        data |= {
            "quantity": quantity + arrival_object.quantity,
            "weight": weight + arrival_object.weight
        }
        object = ArrivalWait.objects.filter(name=name).update(**data)
    else:
        object = ArrivalWait.objects.create(**data)
    return object


def create_or_update_in_stock(data):
    pass
