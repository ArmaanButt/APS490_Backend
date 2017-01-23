import json
from marshmallow import ValidationError


# converts sql row to dict
def build_object(row):
    d = {}
    if row is None:
        return d

    for column in row.__table__.columns:
        # TODO: Need try-except for python2.7 inside docker container
        # After figuring out venv inside docker, relative imports
        # remove this hack
        try:
            a = str(getattr(row, column.name))
        except UnicodeEncodeError:
            a = getattr(row, column.name).encode('utf-8')
        d[column.name] = a

    return d


# converts sql rows to list of dicts
def build_objects(rows):
    return [build_object(row) for row in rows]


# helper for PATCH
def update_model(resource, model):
    for k, v in resource.items():
        if v is not None:
            model.__setattr__(k, v)


# converts returned data to json; used in tests
def to_json(data):
    return json.loads(data.data.decode('utf8'))


def validate_data(schema, params):
    errors = schema.validate(data=params)
    if errors:
        raise ValidationError(errors)


def convert_to_boolean(value):
    """
    >>> convert_to_boolean(True)
    True
    >>> convert_to_boolean('True')
    True
    >>> convert_to_boolean('true')
    True
    >>> convert_to_boolean('1')
    True
    >>> convert_to_boolean(1)
    True
    >>> convert_to_boolean('False')
    False
    """
    truthy = {'t', 'T', 'true', 'True', 'TRUE', '1', 1, True}
    falsy = {'f', 'F', 'false', 'False', 'FALSE', '0', 0, 0.0, False}
    if value is None:
        return None
    elif value in truthy:
        return True
    elif value in falsy:
        return False

    return bool(value)


if __name__ == '__main__':
    from doctest import testmod
    testmod()
