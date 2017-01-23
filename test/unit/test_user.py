import json
from test.backendtestcase import TestCase
from app.utils.utils import to_json


D_URL = '/users/{id}'


class UserEndpointTestCase(TestCase):
    def setUp(self):
        super(UserEndpointTestCase, self).setUp()
        self.data1 = {
            'username': '123456789',
            'password': 'joe123',
            'role': 'admin',
        }
        self.data2 = {
            'username': '345231239',
            'password': 'jack123',
            'role': 'general',
        }
        self.test_client.post(
            '/users',
            data=json.dumps(self.data1),
            content_type='application/json',
        )

    # Collection
    def test_get_collection(self):
        response = self.test_client.get('/users')
        self.assertEqual(response.status_code, 200)
        data = to_json(response)
        self.assertEqual(self.data1['username'], data[0]['username'])
        self.assertEqual(self.data1['role'], data[0]['role'])

    def test_get_collection_with_params(self):
        # setup
        self.test_client.post(
            '/users',
            data=json.dumps(self.data2),
            content_type='application/json',
        )

        response = self.test_client.get('/users?role=admin')
        self.assertEqual(response.status_code, 200)
        data = to_json(response)
        self.assertEqual(len(data), 1)
        self.assertEqual(self.data1['username'], data[0]['username'])
        self.assertEqual(self.data1['role'], data[0]['role'])

        response = self.test_client.get('/users?username=123')
        data = to_json(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 0)

    def test_get_colection_with_invalid_params(self):
        response = self.test_client.get('/users?role=admin1')
        data = to_json(response)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], {
            'role': ['Role must be admin or general'],
        })

    def test_post_collection(self):
        response = self.test_client.post(
            '/users',
            data=json.dumps(self.data2),
            content_type='application/json',
        )
        data = to_json(response)
        assert(data['id'])
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['username'], self.data2['username'])
        self.assertEqual(data['role'], self.data2['role'])

    def test_post_collection_missing_fields(self):
        new_data = {'username': '234234234'}
        response = self.test_client.post(
            '/users',
            data=json.dumps(new_data),
            content_type='application/json',
        )
        data = to_json(response)
        self.assertEqual(data['error'], {
            'password': ['Missing data for required field.'],
            'role': ['Missing data for required field.'],
        })
        self.assertEqual(response.status_code, 400)

    def test_post_collection_duplicate(self):
        response = self.test_client.post(
            '/users',
            data=json.dumps(self.data1),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 409)

    def test_get_detail(self):
        response = self.test_client.get('/users')
        data1 = to_json(response)[0]
        id = data1['id']

        response = self.test_client.get(D_URL.format(id=id))
        data2 = to_json(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data1, data2)

    def test_get_detail_invalid(self):
        # invalid id
        id = 999

        response = self.test_client.get(D_URL.format(id=id))
        data = to_json(response)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['error'], 'Not found!')

    def test_patch_detail(self):
        # setup
        data = to_json(
            self.test_client.post(
                '/users',
                data=json.dumps(self.data2),
                content_type='application/json',
            )
        )
        id = data['id']
        new_data = {'role': 'admin'}
        response = self.test_client.patch(
            D_URL.format(id=id),
            data=json.dumps(new_data),
            content_type='application/json',
        )
        data = to_json(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['id'], id)
        self.assertEqual(data['username'], self.data2['username'])
        self.assertEqual(data['role'], new_data['role'])

    def test_patch_detail_invalid(self):
        # invalid id
        id = 999
        new_data = {'role': 'admin'}
        response = self.test_client.patch(
            D_URL.format(id=id),
            data=json.dumps(new_data),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 404)

    def test_patch_detail_invalid_data(self):
        # setup
        data = to_json(
            self.test_client.post(
                '/users',
                data=json.dumps(self.data2),
                content_type='application/json',
            )
        )
        id = data['id']
        new_data = {'role': 'admin1111'}
        response = self.test_client.patch(
            D_URL.format(id=id),
            data=json.dumps(new_data),
            content_type='application/json',
        )
        data = to_json(response)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], {
            'role': ['Role must be admin or general'],
        })

    def test_delete_detail(self):
        # setup
        data = to_json(
            self.test_client.post(
                '/users',
                data=json.dumps(self.data2),
                content_type='application/json',
            )
        )
        id = data['id']
        response = self.test_client.delete(D_URL.format(id=id))
        self.assertEqual(response.status_code, 204)

        response = self.test_client.get(D_URL.format(id=id))
        self.assertEqual(response.status_code, 404)

    def test_delete_detail_invalid(self):
        # invalid id
        id = 999
        response = self.test_client.delete(D_URL.format(id=id))
        data = to_json(response)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['error'], 'Not found!')
