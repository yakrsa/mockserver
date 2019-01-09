# -*- coding:utf-8 -*-
import sys
from tornado.gen import coroutine
import tornado.ioloop
import tornado.web
from tornado.httpclient import AsyncHTTPClient
from mock_processor import MockProcessor

from config import DOMAIN

# 定义处理类型


class MainHandler(tornado.web.RequestHandler):
    mock_processor = MockProcessor()

    def get_client_ip(self):
        header = dict(self.request.headers)
        client_ip = header.get("DEVICE_IP")
        if client_ip is None:
            client_ip = self.request.remote_ip
        return client_ip

    @coroutine
    def get(self, *args, **kwargs):
        uri = self.request.uri
        print uri
        params = self.request.arguments.keys()
        req_params = {}
        for param in params:
            param_value = self.request.arguments.get(param)[0]
            req_params.update({param: param_value})
        print req_params
        path_name = uri.split("?")[0]
        response = tornado.gen.Return(
            self.mock_processor.mock_response(
                path_name=path_name,
                req_ip=self.get_client_ip(),
                http_method="GET",
                req_params=req_params))

        response = response.args[0]
        res_status_code = response.get("res_status_code")
        res_body = response.get("res_body")
        res_header = response.get("res_header")
        if res_body is None and res_header is None:
            client = AsyncHTTPClient()
            # 转发到真实服务
            url = DOMAIN + uri
            response = yield client.fetch(request=url, headers=self.request.headers, method="GET", validate_cert=False,
                                          request_timeout=60)
            res_header = dict(response.headers)
            res_body = response.body
            res_status_code = response.code

        for k in res_header.keys():
            if k.lower() == "set-cookie":
                cookie = res_header.get(k)
                cks = cookie.split(",")
                for ck in cks:
                    self.add_header(k, ck)
                continue
            self.set_header(k, res_header.get(k))
        self.clear_header("Content-Encoding")
        self.clear_header("Transfer-Encoding")
        self.set_status(res_status_code)
        if res_body is not None and res_body != "":
            self.write(res_body)
        self.finish()

    @coroutine
    def post(self, *args, **kwargs):
        uri = self.request.uri
        req_params = self.request.body
        response = tornado.gen.Return(
            self.mock_processor.mock_response(path_name=uri, req_ip=self.get_client_ip(), http_method="POST",
                                              req_params=req_params))

        response = response.args[0]
        res_status_code = response.get("res_status_code")
        res_body = response.get("res_body")
        res_header = response.get("res_header")
        if res_body is None and res_header is None:
            client = AsyncHTTPClient()
            # 转发到真实服务
            url = DOMAIN + uri
            response = yield client.fetch(request=url, headers=self.request.headers, method="POST",
                                          body=self.request.body, validate_cert=False, request_timeout=60)

            res_header = dict(response.headers)
            res_body = response.body
            res_status_code = response.code

        for k in res_header.keys():
            if k.lower() == "set-cookie":
                cookie = res_header.get(k)
                cks = cookie.split(",")
                for ck in cks:
                    self.add_header(k, ck)
                continue
            self.set_header(k, res_header.get(k))
        self.clear_header("Content-Encoding")
        self.clear_header("Transfer-Encoding")
        self.set_status(res_status_code)
        if res_body is not None and res_body != "":
            self.write(res_body)
        self.finish()

    @coroutine
    def delete(self, *args, **kwargs):
        uri = self.request.uri
        req_params = self.request.body
        response = tornado.gen.Return(
            self.mock_processor.mock_response(path_name=uri, req_ip=self.get_client_ip(), http_method="DELETE",
                                              req_params=req_params))

        response = response.args[0]
        res_status_code = response.get("res_status_code")
        res_body = response.get("res_body")
        res_header = response.get("res_header")
        if res_body is None and res_header is None:
            client = AsyncHTTPClient()
            # 转发到真实服务
            url = DOMAIN + uri
            response = yield client.fetch(request=url, headers=self.request.headers, method="DELETE",
                                          body=self.request.body, validate_cert=False, request_timeout=60)
            res_header = dict(response.headers)
            res_body = response.body
            res_status_code = response.code

        for k in res_header.keys():
            if k.lower() == "set-cookie":
                cookie = res_header.get(k)
                cks = cookie.split(",")
                for ck in cks:
                    self.add_header(k, ck)
                continue
            self.set_header(k, res_header.get(k))
        self.clear_header("Content-Encoding")
        self.clear_header("Transfer-Encoding")
        self.set_status(res_status_code)
        if res_body is not None and res_body != "":
            self.write(res_body)
        self.finish()

    @coroutine
    def options(self, *args, **kwargs):
        uri = self.request.uri
        req_params = self.request.body
        response = tornado.gen.Return(
            self.mock_processor.mock_response(path_name=uri, req_ip=self.get_client_ip(), http_method="OPTIONS",
                                              req_params=req_params))

        response = response.args[0]
        res_status_code = response.get("res_status_code")
        res_body = response.get("res_body")
        res_header = response.get("res_header")
        if res_body is None and res_header is None:
            client = AsyncHTTPClient()
            # 转发到真实服务
            url = DOMAIN + uri
            response = yield client.fetch(request=url, headers=self.request.headers, method="OPTIONS",
                                          body=self.request.body, validate_cert=False, request_timeout=60)
            res_header = dict(response.headers)
            res_body = response.body
            res_status_code = response.code

        for k in res_header.keys():
            if k.lower() == "set-cookie":
                cookie = res_header.get(k)
                cks = cookie.split(",")
                for ck in cks:
                    self.add_header(k, ck)
                continue
            self.set_header(k, res_header.get(k))
        self.clear_header("Content-Encoding")
        self.clear_header("Transfer-Encoding")
        self.set_status(res_status_code)
        if res_body is not None and res_body != "":
            self.write(res_body)
        self.finish()

    @coroutine
    def head(self, *args, **kwargs):
        uri = self.request.uri
        req_params = self.request.body
        response = tornado.gen.Return(
            self.mock_processor.mock_response(path_name=uri, req_ip=self.get_client_ip(), http_method="HEAD",
                                              req_params=req_params))

        response = response.args[0]
        res_status_code = response.get("res_status_code")
        res_body = response.get("res_body")
        res_header = response.get("res_header")
        if res_body is None and res_header is None:
            client = AsyncHTTPClient()
            # 转发到真实服务
            url = DOMAIN + uri
            response = yield client.fetch(request=url, headers=self.request.headers, method="HEAD",
                                          body=self.request.body, validate_cert=False, request_timeout=60)
            res_header = dict(response.headers)
            res_body = response.body
            res_status_code = response.code

        for k in res_header.keys():
            if k.lower() == "set-cookie":
                cookie = res_header.get(k)
                cks = cookie.split(",")
                for ck in cks:
                    self.add_header(k, ck)
                continue
            self.set_header(k, res_header.get(k))
        self.clear_header("Content-Encoding")
        self.clear_header("Transfer-Encoding")
        self.set_status(res_status_code)
        if res_body is not None and res_body != "":
            self.write(res_body)
        self.finish()

    @coroutine
    def put(self, *args, **kwargs):
        uri = self.request.uri
        req_params = self.request.body
        response = tornado.gen.Return(
            self.mock_processor.mock_response(path_name=uri, req_ip=self.get_client_ip(), http_method="PUT",
                                              req_params=req_params))

        response = response.args[0]
        res_status_code = response.get("res_status_code")
        res_body = response.get("res_body")
        res_header = response.get("res_header")
        if res_body is None and res_header is None:
            client = AsyncHTTPClient()
            # 转发到真实服务
            url = DOMAIN + uri
            response = yield client.fetch(request=url, headers=self.request.headers, method="PUT",
                                          body=self.request.body, validate_cert=False, request_timeout=60)
            res_header = dict(response.headers)
            res_body = response.body
            res_status_code = response.code

        for k in res_header.keys():
            if k.lower() == "set-cookie":
                cookie = res_header.get(k)
                cks = cookie.split(",")
                for ck in cks:
                    self.add_header(k, ck)
                continue
            self.set_header(k, res_header.get(k))
        self.clear_header("Content-Encoding")
        self.clear_header("Transfer-Encoding")
        self.set_status(res_status_code)
        if res_body is not None and res_body != "":
            self.write(res_body)
        self.finish()

    @coroutine
    def patch(self, *args, **kwargs):
        uri = self.request.uri
        req_params = self.request.body
        response = tornado.gen.Return(
            self.mock_processor.mock_response(path_name=uri, req_ip=self.get_client_ip(), http_method="PATCH",
                                              req_params=req_params))

        response = response.args[0]
        res_status_code = response.get("res_status_code")
        res_body = response.get("res_body")
        res_header = response.get("res_header")
        if res_body is None and res_header is None:
            client = AsyncHTTPClient()
            # 转发到真实服务
            url = DOMAIN + uri
            response = yield client.fetch(request=url, headers=self.request.headers, method="PATCH",
                                          body=self.request.body, validate_cert=False, request_timeout=60)
            res_header = dict(response.headers)
            res_body = response.body
            res_status_code = response.code

        for k in res_header.keys():
            if k.lower() == "set-cookie":
                cookie = res_header.get(k)
                cks = cookie.split(",")
                for ck in cks:
                    self.add_header(k, ck)
                continue
            self.set_header(k, res_header.get(k))
        self.clear_header("Content-Encoding")
        self.clear_header("Transfer-Encoding")
        self.set_status(res_status_code)
        if res_body is not None and res_body != "":
            self.write(res_body)
        self.finish()


if __name__ == "__main__":
    # 创建一个应用对象
    app = tornado.web.Application([(r'/', MainHandler),
                                   (r".*", MainHandler)])
    # 绑定一个监听端口
    port = 9898
    try:
        if len(sys.argv) > 1:
            port = int(sys.argv[1])
    except Exception as e:
        print e
        print "default port is: ", port
    app.listen(port)
    print "tornado started on port %s" % port
    # 启动web程序，开始监听端口的连接
    tornado.ioloop.IOLoop.current().start()
