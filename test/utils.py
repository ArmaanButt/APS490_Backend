import json
from app.utils.utils import to_json


def post_data(test_client, url, data):
    response = test_client.post(
        url,
        data=json.dumps(data),
        content_type='application/json',
    )
    response_data = to_json(response)
    return response_data['id']


def second_equals_first(first, second):
    for key in first:
        assert first[key] == second[key]
