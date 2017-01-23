import json
from test.backendtestcase import TestCase
from test.utils import post_data, second_equals_first
from app.utils.utils import to_json


C_URL = '/shots'
D_URL = '/shots/{id}'


class ShotEndpointTestCase(TestCase):
    def setUp(self):
        super(ShotEndpointTestCase, self).setUp()
        self.user_id = post_data(
            test_client=self.test_client,
            url='/users',
            data={
                'username': '1234',
                'password': 'joe123',
                'role': 'admin',
            },
        )
        self.target_id1 = post_data(
            test_client=self.test_client,
            url='/targets',
            data={
                'is_working': False,
                'size': 100,
                'is_enabled': False,
            },
        )
        self.target_id2 = post_data(
            test_client=self.test_client,
            url='/targets',
            data={
                'is_working': False,
                'size': 100,
                'is_enabled': False,
            },
        )
        self.session_id1 = post_data(
            test_client=self.test_client,
            url='/sessions',
            data={
                'user_id': self.user_id,
                'target_id': self.target_id1,
            },
        )
        self.shot1_data = {
            'user_id': self.user_id,
            'target_id': self.target_id1,
            'session_id': self.session_id1,
            'coordinate_x': 56.2,
            'coordinate_y': 9.3,
        }
        self.shot_id1 = post_data(
            test_client=self.test_client,
            url=C_URL,
            data=self.shot1_data,
        )

    def test_get_collection(self):
        response = self.test_client.get(C_URL)
        data = to_json(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        second_equals_first(
            self.shot1_data,
            data[0],
        )

    def test_get_collection_with_params(self):
        # setup
        new_data = self.shot1_data
        new_data['target_id'] = self.target_id2
        self.test_client.post(
            C_URL,
            data=json.dumps(new_data),
            content_type='application/json',
        )

        response = self.test_client.get(
            C_URL + '?user_id=' + str(self.user_id),
        )
        data = to_json(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)

        response = self.test_client.get(
            C_URL + '?target_id=' + str(self.target_id1),
        )
        data = to_json(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)

    def test_get_colection_with_invalid_params(self):
        response = self.test_client.get(
            C_URL + '?user_id=abc',
        )
        data = to_json(response)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], {
            'user_id': ['Not a valid integer.'],
        })

    def test_post_collection(self):
        new_data = {
            'user_id': self.user_id,
            'target_id': self.target_id1,
            'session_id': self.session_id1,
            'coordinate_x': 120.23,
            'coordinate_y': 10.4,
        }
        response = self.test_client.post(
            C_URL,
            data=json.dumps(new_data),
            content_type='application/json',
        )
        data = to_json(response)
        assert (data['id'])
        self.assertEqual(response.status_code, 201)
        second_equals_first(new_data, data)

    def test_post_collection_missing_fields(self):
        new_data = {'user_id': self.user_id}
        response = self.test_client.post(
            C_URL,
            data=json.dumps(new_data),
            content_type='application/json',
        )
        data = to_json(response)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], {
            'target_id': ['Missing data for required field.'],
            'session_id': ['Missing data for required field.'],
            'coordinate_x': ['Missing data for required field.'],
            'coordinate_y': ['Missing data for required field.'],
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
        data1 = to_json(self.test_client.get(D_URL.format(id=self.shot_id1)))

        id = data1['id']
        new_data = {
            'target_id': self.target_id2,
            'coordinate_x': 100.100,
        }
        response = self.test_client.patch(
            D_URL.format(id=id),
            data=json.dumps(new_data),
            content_type='application/json',
        )
        data2 = to_json(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data2['id'], id)
        self.assertEqual(data2['target_id'], new_data['target_id'])
        self.assertEqual(data2['coordinate_x'], new_data['coordinate_x'])
        self.assertNotEqual(data2['updated_at'], data1['updated_at'])

    def test_patch_detail_invalid(self):
        # invalid id
        id = 999
        new_data = {'target_id': self.target_id2}
        response = self.test_client.patch(
            D_URL.format(id=id),
            data=json.dumps(new_data),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 404)

    def test_patch_detail_invalid_data(self):
        # setup
        data1 = to_json(self.test_client.get(D_URL.format(id=self.shot_id1)))
        id = data1['id']
        new_data = {
            'target_id': self.target_id2,
            'coordinate_x': 'abc',
        }
        response = self.test_client.patch(
            D_URL.format(id=id),
            data=json.dumps(new_data),
            content_type='application/json',
        )
        data = to_json(response)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], {
            'coordinate_x': ['Not a valid number.'],
        })

    def test_delete_detail(self):
        response = self.test_client.get(D_URL.format(id=self.shot_id1))
        self.assertEqual(response.status_code, 200)

        response = self.test_client.delete(D_URL.format(id=self.shot_id1))
        self.assertEqual(response.status_code, 204)

        response = self.test_client.get(D_URL.format(id=self.shot_id1))
        self.assertEqual(response.status_code, 404)

    def test_delete_detail_invalid(self):
        # invalid id
        id = 999
        response = self.test_client.delete(D_URL.format(id=id))
        data = to_json(response)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['error'], 'Not found!')
