import json
from test.backendtestcase import TestCase
from app.utils.utils import to_json


C_URL = '/targets'
D_URL = '/targets/{id}'


class TargetEndpointTestCase(TestCase):
    def setUp(self):
        super(TargetEndpointTestCase, self).setUp()
        self.data1 = {
            'is_working': False,
            'size': 100,
            'is_enabled': False,
        }
        self.data2 = {
            'is_working': True,
            'size': 34.56,
            'is_enabled': False,
        }
        self.test_client.post(
            C_URL,
            data=json.dumps(self.data1),
            content_type='application/json',
        )

    def test_get_collection(self):
        response = self.test_client.get(C_URL)
        data = to_json(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        assert(data[0]['id'])
        self._is_equal(self.data1, data[0])

    def test_get_collection_with_params(self):
        # setup
        self.test_client.post(
            C_URL,
            data=json.dumps(self.data2),
            content_type='application/json',
        )

        response = self.test_client.get(C_URL + '?is_working=False')
        data = to_json(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        assert (data[0]['id'])
        self._is_equal(self.data1, data[0])

        response = self.test_client.get(C_URL + '?is_enabled=False')
        data = to_json(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)

    def test_get_colection_with_invalid_params(self):
        response = self.test_client.get(C_URL + '?is_working=123')
        data = to_json(response)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], {
            'is_working': ['Not a valid boolean.'],
        })

    def test_post_collection(self):
        response = self.test_client.post(
            C_URL,
            data=json.dumps(self.data2),
            content_type='application/json',
        )
        data = to_json(response)
        assert (data['id'])
        self.assertEqual(response.status_code, 201)
        self._is_equal(self.data2, data)

    def test_post_collection_missing_fields(self):
        new_data = {'is_working': False}
        response = self.test_client.post(
            C_URL,
            data=json.dumps(new_data),
            content_type='application/json',
        )
        data = to_json(response)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], {
            'size': ['Missing data for required field.'],
            'is_enabled': ['Missing data for required field.'],
        })

    def test_get_detail(self):
        response = self.test_client.get(C_URL)
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
        data1 = to_json(
            self.test_client.post(
                C_URL,
                data=json.dumps(self.data2),
                content_type='application/json',
            )
        )
        id = data1['id']
        new_data = {'is_enabled': True, 'id': 12, 'image_name': 'abc.jpg'}
        response = self.test_client.patch(
            D_URL.format(id=id),
            data=json.dumps(new_data),
            content_type='application/json',
        )
        data2 = to_json(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data2['id'], id)
        # all fields same, except `is_enabled`
        self.assertEqual(data2['is_working'], self.data2['is_working'])
        self.assertEqual(data2['size'], self.data2['size'])
        self.assertEqual(data2['is_enabled'], new_data['is_enabled'])
        self.assertEqual(data2['image_name'], new_data['image_name'])
        self.assertNotEqual(data2['updated_at'], data1['updated_at'])

    def test_patch_detail_invalid(self):
        # invalid id
        id = 999
        new_data = {'is_enabled': True}
        response = self.test_client.patch(
            D_URL.format(id=id),
            data=json.dumps(new_data),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 404)

    def test_patch_detail_invalid_data(self):
        # setup
        data1 = to_json(
            self.test_client.post(
                C_URL,
                data=json.dumps(self.data2),
                content_type='application/json',
            )
        )
        id = data1['id']

        new_data = {'size': 'abc'}
        response = self.test_client.patch(
            D_URL.format(id=id),
            data=json.dumps(new_data),
            content_type='application/json',
        )
        data = to_json(response)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], {'size': ['Not a valid number.']})

    def test_delete_detail(self):
        # setup
        data = to_json(
            self.test_client.post(
                C_URL,
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

    def _is_equal(self, first, second):
        for key in first:
            self.assertEqual(first[key], second[key])
