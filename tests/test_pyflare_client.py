__author__ = 'Joe Linn'

import unittest
from pyflare import PyflareClient
from mock_responses import mock_response_client


class PyflareTest(unittest.TestCase):
    def setUp(self):
        self.pyflare = PyflareClient('address@example.com', 'your_api_key')

    @mock_response_client
    def test_stats(self):
        response = self.pyflare.stats('example.com', 40)
        time_zero = response['response']['result']['timeZero']
        self.assertTrue(isinstance(time_zero, int) or isinstance(time_zero, long))

    @mock_response_client
    def test_zone_load_multi(self):
        response = self.pyflare.zone_load_multi()
        self.assertIsInstance(response['response']['zones']['count'], int)

    @mock_response_client
    def test_rec_load_all(self):
        for response in self.pyflare.rec_load_all('example.com'):
            self.assertIsInstance(response['props']['cloud_on'], int)

    @mock_response_client
    def test_zone_check(self):
        response = self.pyflare.zone_check(['example.com'])
        for zone, zid in response['response']['zones'].items():
            self.assertIsInstance(zid, int)

    @mock_response_client
    def test_zone_ips(self):
        response = self.pyflare.zone_ips('example.com')
        self.assertIsInstance(response['response']['ips'], list)

    @mock_response_client
    def test_ip_lkup(self):
        ip = '0.0.0.0'
        response = self.pyflare.ip_lkup(ip)
        self.assertIn(ip, response['response'])

    @mock_response_client
    def test_zone_settings(self):
        response = self.pyflare.zone_settings('example.com')
        self.assertIsInstance(response['response']['result']['objs'], list)

    @mock_response_client
    def test_sec_lvl(self):
        response = self.pyflare.sec_lvl('example.com', 'med')
        self.assertEqual(response['result'], 'success')

    @mock_response_client
    def test_cache_lvl(self):
        response = self.pyflare.cache_lvl('example.com', 'agg')
        self.assertEqual(response['result'], 'success')

    @mock_response_client
    def test_devmode(self):
        response = self.pyflare.devmode('example.com', False)
        self.assertIn('zone_id', response['response']['zone']['obj'])

    @mock_response_client
    def test_fpurge_ts(self):
        response = self.pyflare.fpurge_ts('example.com')
        self.assertIsInstance(response['response']['fpurge_ts'], int)

    @mock_response_client
    def test_zone_file_purge(self):
        response = self.pyflare.zone_file_purge('example.com', 'https://example.com/image.jpg')
        self.assertIn('url', response['response'])
        self.assertEqual(response['result'], 'success')

    @mock_response_client
    def test_zone_grab(self):
        response = self.pyflare.zone_grab(9001)
        self.assertEqual(response['result'], 'success')

    @mock_response_client
    def test_wl(self):
        response = self.pyflare.wl('0.0.0.0')
        self.assertEqual(response['result'], 'success')
        self.assertEqual(response['response']['result']['action'], 'WL')

    @mock_response_client
    def test_ban(self):
        response = self.pyflare.ban('0.0.0.0')
        self.assertEqual(response['result'], 'success')
        self.assertEqual(response['response']['result']['action'], 'BAN')

    @mock_response_client
    def test_nul(self):
        response = self.pyflare.nul('0.0.0.0')
        self.assertEqual(response['result'], 'success')
        self.assertEqual(response['response']['result']['action'], 'NUL')

    @mock_response_client
    def test_ipv46(self):
        response = self.pyflare.ipv46('example.com', False)
        self.assertEqual(response['result'], 'success')

    @mock_response_client
    def test_async(self):
        response = self.pyflare.async('example.com', 0)
        self.assertEqual(response['result'], 'success')

    @mock_response_client
    def test_minify(self):
        response = self.pyflare.minify('example.com', 0)
        self.assertEqual(response['result'], 'success')

    @mock_response_client
    def test_mirage2(self):
        response = self.pyflare.mirage2('example.com', False)
        self.assertEqual(response['result'], 'success')

    @mock_response_client
    def test_rec_new(self):
        response = self.pyflare.rec_new('example.com', 'A', 'sub', '1.2.3.4')
        self.assertIn('rec_id', response['response']['rec']['obj'])

    @mock_response_client
    def test_rec_edit(self):
        response = self.pyflare.rec_edit('example.com', 'A', 9001, 'sub', '1.2.3.4')
        self.assertIn('rec_id', response['response']['rec']['obj'])

    @mock_response_client
    def test_rec_delete(self):
        response = self.pyflare.rec_delete('example.com', 9001)
        self.assertEqual(response['result'], 'success')

if __name__ == '__main__':
    unittest.main()
