from . import new_york
from . import california

def get_inc_records(name):
    entities = []

    entities += new_york.get_inc_records(name)
    entities += california.get_inc_records(name)

    return entities

def get_matching_records(name):
    entities = get_inc_records(name)

    return [entity for entity in entities if entity['name'] == name.upper().replace(',', '').replace('.', '')]
