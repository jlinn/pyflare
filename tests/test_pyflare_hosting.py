__author__ = 'Vanc Levstik'

import unittest
from pyflare import PyflareHosting
from mock_responses import mock_response_hosting


class PyflareTest(unittest.TestCase):
    def setUp(self):
        self.pyflare = PyflareHosting('your_api_key')

    @mock_response_hosting
    def test_host_key_regen(self):
        response = self.pyflare.host_key_regen()
        self.assertEqual(response['result'], 'success')

    @mock_response_hosting
    def test_user_create(self):
        response = self.pyflare.user_create('newuser@example.com', 'password')
        self.assertEqual(
            response['response']['cloudflare_email'],
            'newuser@example.com'
        )

    @mock_response_hosting
    def test_user_create_unique_id(self):
        response = self.pyflare.user_create(
            'newuser@example.com',
            'password',
            unique_id='dummy_id')
        self.assertEqual(
            response['response']['cloudflare_email'],
            'newuser@example.com'
        )

    @mock_response_hosting
    def test_zone_set(self):
        response = self.pyflare.zone_set(
            'user_key',
            'someexample.com',
            'cloudflare-resolve-to.someexample.com',
            'www,blog,wordpress:cloudflare-rs2.someexample.com')

        self.assertEqual(
            response['response']['zone_name'],
            'someexample.com'
        )
        self.assertEqual(
            response['response']['resolving_to'],
            'cloudflare-resolve-to.someexample.com'
        )

    @mock_response_hosting
    def test_full_zone_set(self):
        response = self.pyflare.full_zone_set(
            'user_key',
            'someexample.com')

        self.assertEqual(
            response['response']['zone_name'],
            'someexample.com'
        )
        self.assertEqual(
            response['response']['jumpstart'],
            'true'
        )

    @mock_response_hosting
    def test_user_lookup_email(self):
        response = self.pyflare.user_lookup(
            cloudflare_email='newuser@example.com')
        self.assertEqual(
            response['response']['cloudflare_email'],
            'newuser@example.com'
        )
        self.assertEqual(
            response['response']['unique_id'],
            'someuniqueid'
        )

    @mock_response_hosting
    def test_user_lookup_unique_id(self):
        response = self.pyflare.user_lookup(
            unique_id='someuniqueid')
        self.assertEqual(
            response['response']['cloudflare_email'],
            'newuser@example.com'
        )
        self.assertEqual(
            response['response']['unique_id'],
            'someuniqueid'
        )

    @mock_response_hosting
    def test_user_auth_password(self):
        response = self.pyflare.user_auth(
            cloudflare_email='newuser@example.com',
            cloudflare_pass='password',
        )
        self.assertEqual(
            response['response']['user_key'],
            '8afbe6dea02407989af4dd4c97bb6e25'
        )

    @mock_response_hosting
    def test_user_auth_unique_id(self):
        response = self.pyflare.user_auth(
            unique_id='dummy_id'
        )
        self.assertEqual(
            response['response']['user_key'],
            '8afbe6dea02407989af4dd4c97bb6e25'
        )

    @mock_response_hosting
    def test_zone_lookup(self):
        response = self.pyflare.zone_lookup(
            user_key='user_key',
            zone_name='someexample.com'
        )
        self.assertEqual(
            response['response']['zone_name'],
            'someexample.com'
        )
        self.assertEqual(
            response['response']['zone_exists'],
            'true'
        )

    @mock_response_hosting
    def test_zone_delete(self):
        response = self.pyflare.zone_delete(
            user_key='user_key',
            zone_name='someexample.com'
        )
        self.assertEqual(
            response['response']['zone_name'],
            'someexample.com'
        )
        self.assertEqual(
            response['response']['zone_deleted'],
            'true'
        )

    @mock_response_hosting
    def test_zone_list(self):
        response = self.pyflare.zone_list(
            user_key='user_key',
            limit=10,
            zone_status='V'
        )
        self.assertEqual(
            response['response'][0]['zone_name'],
            'example.com'
        )
        self.assertEqual(
            response['response'][0]['zone_status'],
            'V'
        )


if __name__ == '__main__':
    unittest.main()
