import json
import unittest
from unittest import mock
from requests import HTTPError
from src.agents.helper import Helper


class TestHelpers(unittest.TestCase):
    # This test suite tests various cases of the helper functions in src.agents.helper

    test_dict = json.loads(
        '{"location":{"ip":"31.205.216.21","success":true,"type":"IPv4","continent":"Europe","continent_code":"EU",'
        '"country":"United Kingdom","country_code":"GB","country_flag":"https:\/\/cdn.ipwhois.io\/flags\/gb.svg",'
        '"country_capital":"London","country_phone":"+44","country_neighbours":"IE","region":"England",'
        '"city":"Sheffield","latitude":"53.381129","longitude":"-1.470085","asn":"AS41230","org":"Ask4 Limited",'
        '"isp":"Ask4 Limited","timezone":"Europe\/London","timezone_name":"Greenwich Mean Time",'
        '"timezone_dstOffset":"0","timezone_gmtOffset":"0","timezone_gmt":"GMT 0:00","currency":"British Pound '
        'Sterling","currency_code":"GBP","currency_symbol":"\u00a3","currency_rates":"0.791414",'
        '"currency_plural":"British pounds sterling","completed_requests":24}}')

    # This method will be used by the mock to replace requests.get
    def mocked_requests_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        if args[0] == 'http://someurl.com/success':
            return MockResponse({"key1": "value1"}, 200)
        elif args[0] == 'http://someurl.com/fail':
            return MockResponse({"key2": "value2"}, 400)

        return MockResponse(None, 404)

    # Testing the get_request method
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_get_request_ok(self, mock_get):
        url = "http://someurl.com/success"
        resp = Helper.get_request(url)
        correct_resp = json.loads('{"key1": "value1"}')
        self.assertDictEqual(resp, correct_resp)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_get_request_fail(self, mock_get):
        url = "http://someurl.com/fail"
        # resp = Helper.get_request(url)
        # correct_resp = json.loads('{"key2": "value2"}')
        self.assertRaises(HTTPError, Helper.get_request, url)

    # Testing the get_by_complex_key method
    def test_json_parse_key_present(self):
        key = "location.latitude"
        val = Helper.get_by_complex_key(self.test_dict, key)
        self.assertEqual(val, "53.381129")

    def test_json_parse_key_absent(self):
        key = "location.port"
        val = Helper.get_by_complex_key(self.test_dict, key)
        self.assertEqual(val, "")

    # Testing the interpolate_values method
    def test_interpolate_string_nested(self):
        string = "https://api.sunrise-sunset.org/json?lat={{location.latitude}}&lng={{location.longitude}}"
        correct_val = "https://api.sunrise-sunset.org/json?lat=53.381129&lng=-1.470085"
        val = Helper.interpolate_values(string, self.test_dict)
        self.assertEqual(val, correct_val)

    def test_interpolate_string_non_existing(self):
        string = "https://api.sunrise-sunset.org/json?lat={{location.port}}&lng={{location.longitude}}"
        correct_val = "https://api.sunrise-sunset.org/json?lat=&lng=-1.470085"
        val = Helper.interpolate_values(string, self.test_dict)
        self.assertEqual(val, correct_val)

    def test_interpolate_string_unmatched_brackets(self):
        string = "https://api.sunrise-sunset.org/json?lat={{location.latitude}}&lng={{location.longitude}"
        correct_val = "https://api.sunrise-sunset.org/json?lat=53.381129&lng={{location.longitude}"
        val = Helper.interpolate_values(string, self.test_dict)
        self.assertEqual(val, correct_val)
