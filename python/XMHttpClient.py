#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
__author__ = 'xiaomi passport (xiaomi-account-dev@xiaomi.com)'

'''
Python 3 client SDK for Xiaomi Open API
'''

import urllib.request
import urllib.parse
import json
from urllib.parse import urljoin

class XMHttpClient(object):
    def __init__(self, url: str):
        self.url = url

    def get(self, path: str, params: dict, header: dict = {}):
        return self.request(path, 'GET', params, header)

    def post(self, path: str, params: dict, header: dict = {}):
        return self.request(path, 'POST', params, header)

    # 发送 HTTP 请求
    def request(self, path: str, method: str, params: dict = None, headers: dict = {}):
        if method not in ('GET', 'POST'):
            raise ValueError(f"Invalid HTTP method: {method}")

        data = self.buildQueryString(params)
        http_url = f"{urljoin(self.url, path)}?{data}" if method == 'GET' else urljoin(self.url, path)
        post_data = data.encode('utf-8') if method == 'POST' and data else None

        req = urllib.request.Request(http_url, data=post_data, headers=headers, method=method)

        try:
            with urllib.request.urlopen(req) as res:
                return res
        except urllib.error.HTTPError as e:
            raise e

    def buildQueryString(self, params: dict):
        if not params or not isinstance(params, dict):
            return ''
        return urllib.parse.urlencode(params)

    # 处理服务器返回的 JSON 字符串（可能前缀不标准）
    def safeJsonLoad(self, jsonStr: bytes):
        jsonStr = jsonStr.decode('utf-8', errors='ignore')
        start = jsonStr.find('{')
        if start == -1:
            start = jsonStr.find('[')
        if start >= 0:
            try:
                return json.loads(jsonStr[start:])
            except json.JSONDecodeError:
                return None
        return None
