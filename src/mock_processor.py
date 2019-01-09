# -*- coding:utf-8 -*-
import time
from dbhelper import DbHelper
from config import DB_HOST, DB_PORT


def compare_dict(dict1, dict2):
    is_equal = True
    for key1 in dict1.keys():
        value1 = dict1.get(key1)
        value2 = dict2.get(key1)
        if type(value1) == unicode:
            value1 = str(value1)
        if type(value2) == unicode:
            value1 = str(value2)
        if not isinstance(value1, type(value2)):
            is_equal = False
            break
        if type(value1) in [type(None), str, int, float, bool, list]:
            if value1 != value2:
                is_equal = False
                break
        elif type(value1)in [dict]:
            is_equal = compare_dict(value1, value2)
            if not is_equal:
                break
        else:
            print type(value1)
            raise Exception

    return is_equal


class MockProcessor(object):
    groups = {}
    projects = {}
    interfaces = {}
    dbhelper = None

    def __init__(self):
        self.dbhelper = DbHelper(host=DB_HOST, port=DB_PORT)

    def mock_response(self, path_name, http_method, req_ip, req_params):
        res_body = None
        res_header = None
        res_status_code = 200
        res_delay = 0
        mock_interface = self.dbhelper.find_interface(
            path_name=path_name, http_method=http_method)
        if mock_interface:
            mock_scenes = mock_interface.get("mock_scene")
            for mock_scene in mock_scenes:
                filter_rule = mock_scene.get("filter_rule")
                mock_response = mock_scene.get("mock_response")
                filter_ip = filter_rule.get("ip","")
                if filter_ip in [None,"", req_ip]:
                    filter_params = filter_rule.get("params","")
                    if filter_params=="" or compare_dict(
                            filter_params, req_params):
                        res_body = mock_response.get("res_body")
                        res_header = mock_response.get("res_header")
                        res_status_code = mock_response.get("res_status_code")
                        res_delay = mock_response.get("delay")
            if res_delay > 0:
                time.sleep(res_delay)
        response = {
            "res_body": res_body,
            "res_header": res_header,
            "res_status_code": res_status_code
        }
        return response


if __name__ == "__main__":
    a = {
        "a": 123,
        "b": "abc",
        44: {
            "aa": "bb",
            "bb": False,
            "cc": {
                "aa": "bb",
                "dd": [1, 3, 2, 3, 4]
            }
        }
    }

    b = {
        "a": 123,
        "b": "abc",
        44: {
            "aa": "bb",
            "bb": False,
            "cc": {
                "aa": "bb",
                "dd": [1, 3, 2, 3, 4]
            }
        }
    }
    print compare_dict(a, b)
