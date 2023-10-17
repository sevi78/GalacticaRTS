import ctypes


def delete_all_references(attacker, defender):
    for key, value in attacker.__dict__.items():
        if defender == value:
            setattr(attacker, key, None)

    for key, value in defender.__dict__.items():
        if attacker == value:
            setattr(defender, key, None)


def get_all_references(obj):
    # do something with my_object
    ref_count = ctypes.c_long.from_address(id(obj))
    return ref_count
