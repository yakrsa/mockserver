# -*- coding:utf-8 -*-
from pymongo import MongoClient
import json


class DbHelper(object):
    con = None
    db = None

    def __init__(self, host='127.0.0.1', port=27017):
        self.conn = MongoClient(host, port)
        self.db = self.conn["yapi"]

    def find_interface(self, path_name, http_method):
        if path_name is None:
            path_name = ""
        path_name = path_name.strip()
        http_method = http_method.strip().upper()

        res = []

        if path_name:
            interfaces = self.db["interface"].find(
                {"path": path_name, "method": http_method})
        else:
            interfaces = self.db["interface"].find()
        for interface in interfaces:
            # 暂时不需要其它属性，只需要interface_id 去查询mock场景
            res.append(
                {
                    "api": path_name,
                    "http_method": http_method,
                    "interface_id": interface.get("_id")
                }
            )
        if res:
            # 正常情况下一个接口应该只有一条记录，所以默认取第一条
            mock_scene = self.find_mock_scene(
                interface_id=res[0].get("interface_id"))
            res[0].update({"mock_scene": mock_scene})
            return res[0]
        else:
            return None

    def find_mock_scene(self, interface_id=0):
        scenes = self.db["adv_mock_case"].find(
            {"interface_id": interface_id, "case_enable": True})
        mock_scene = []
        for scene in scenes:
            res_header = scene.get("headers")
            res_header = [
                item for item in res_header if item.get('_id') is None]
            headers = {}
            for header in res_header:
                header_name = header.keys()[0]
                header_value = header.get(header_name)
                headers.update({header_name:header_value})
            mock_scene.append(
                {
                    "filter_rule": {
                        "ip": scene.get("ip"),
                        "params": scene.get("params")
                    },
                    "mock_response": {
                        "res_body": scene.get("res_body"),
                        "res_header": headers,
                        "res_status_code" : scene.get("code"),
                        "res_delay" : scene.get("delay")
                    }
                }
            )
        return mock_scene


if __name__ == "__main__":
    dbhelper = DbHelper(host="192.168.58.130", port=27017)
    r = dbhelper.find_interface(
        path_name="/quotes-search/api/v2/stocks",
        http_method="get")
    # s = dbhelper.find_mock_scene(interface_id=r.get("_id"))
    print json.dumps(r)
