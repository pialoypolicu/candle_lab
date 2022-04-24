from core_storage.models import Purchase



def create_position(data):
    try:
        obj = Purchase.objects.create(**data)
    except TypeError as error:
        print("Error in create_position", error)
        return {"Message": "wrong data"}
    return {f"Object {obj.name} created"}
