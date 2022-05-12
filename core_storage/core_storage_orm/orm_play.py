import datetime

from django.core.exceptions import ObjectDoesNotExist
from pprint import pprint
from core_storage.models import InStock


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
