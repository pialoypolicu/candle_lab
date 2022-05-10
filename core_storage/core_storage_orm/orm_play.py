import datetime

from django.core.exceptions import ObjectDoesNotExist
from pprint import pprint
from core_storage.models import Purchase, ArrivalWait, InStock


def create_or_update_arrival_wait(data):
    del data['date_purchase']
    del data['price']
    name = data['catalog_name']
    weight = data['weight']
    exist_object_in_arrival = ArrivalWait.objects.filter(catalog_name=name, weight=weight).exists()
    if exist_object_in_arrival:
        quantity = data['quantity']
        arrival_object = ArrivalWait.objects.filter(catalog_name=name, weight=weight)
        if len(arrival_object) != 1:
            return {
                "result": "error",
                "message": "arrival_wait_object is not 1"
            }
        data |= {
            "quantity": quantity + arrival_object.first().quantity,
        }
        arrival_object.update(**data)
        arrival_object = ArrivalWait.objects.filter(catalog_name=name, weight=weight).first()
    else:
        arrival_object = ArrivalWait.objects.create(**data)
    return {"result": arrival_object}


def create_or_update_instock(data):
    name = data['name']
    weight = data['quantity'] * data['weight']
    try:
        instock_object = InStock.objects.get(name=name)
    except ObjectDoesNotExist as error:
        instock_object = None
        print(error)

    if instock_object:
        weight += instock_object.weight
        time_now = datetime.datetime.now()
        update_object_instock = InStock.objects.filter(name=name).update(name=name, weight=weight, update_date=time_now)
        return update_object_instock
    else:
        create_object_instock = InStock.objects.create(name=name, weight=weight)
        return create_object_instock

def delete_or_update_arrival_wait(data):
    name = data['name']
    quantity = data['quantity']
    arrival_object = ArrivalWait.objects.get(name=name)
    total_quantity = arrival_object.quantity - quantity
    # TODO: сделать исклбючение, если значение превышает остаток
    if total_quantity <= 0:
        ArrivalWait.objects.filter(name=name).delete()
        return {"result_arrival_object": "deleted"}
    else:
        ArrivalWait.objects.filter(name=name).update(quantity=total_quantity)
        return {"result_arrival_object": "updated"}



