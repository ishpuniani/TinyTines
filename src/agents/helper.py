import re
import requests
from requests import HTTPError


class Helper:
    @classmethod
    def get_by_complex_key(cls, json_dict, key):
        key_arr = key.strip().split('.')
        value = ""
        d = json_dict.copy()
        for k in key_arr:
            if k not in d.keys():
                d = ''
                break
            else:
                d = d[k]
        value = d
        return value

    @classmethod
    def interpolate_values(cls, string, json_dict):
        str_cpy = string
        try:
            pattern = re.compile(r"{{[a-z|.|_]*}}")
            for match in re.findall(pattern, str_cpy):
                match_str = match.replace('{{', '').replace('}}', '')
                value = cls.get_by_complex_key(json_dict, match_str)
                str_cpy = str_cpy.replace(match, str(value))
        except Exception as e:
            print("Error interpolating values for string: " + string)
            print(e)
            raise Exception(e)
        # print("Interpolated string: " + str_cpy)
        return str_cpy

    @classmethod
    def get_request(cls, url):
        # print("Getting url:: " + url)
        retry_count = 0
        data = {}
        while True:
            try:
                response = requests.get(url)
                if response.status_code != 200:
                    raise HTTPError('Get Request failed')
                data = response.json()
                break
            except HTTPError as e:
                if retry_count < 3:
                    retry_count += 1
                    print("Error getting url:: " + url + ", retry: " + str(retry_count))
                else:
                    print("Unable to get url: " + url)
                    print(e)
                    raise e
        # print("request output:: " + str(data))
        return data
