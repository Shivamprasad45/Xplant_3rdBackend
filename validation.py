from cerberus import Validator

user_schema = {
    'name': {'type': 'string', 'required': True},
    'email': {'type': 'string', 'required': True}
}

plant_schema = {
    'name': {'type': 'string', 'required': True},
    'species': {'type': 'string', 'required': True},
    'age': {'type': 'integer'},
    'planted_date': {'type': 'string',"default":"4546"}
}

def validate_user(data):
    v = Validator(user_schema)
    return v.validate(data), v.errors

def validate_plant(data):
    v = Validator(plant_schema)
    return v.validate(data), v.errors
