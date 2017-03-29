import requests

# URL = 'http://169.254.160.8:5000/shots'
URL = 'http://localhost:5000/shots'


def post_to_api(coordinate_x, coordinate_y):
    payload = {
        'coordinate_x': coordinate_x,
        'coordinate_y': coordinate_y,
    }
    response = requests.request(method='POST', url=URL, json=payload)
    print(response.json())
