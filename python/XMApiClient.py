#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
__author__ = 'xiaomi passport (xiaomi-account-dev@xiaomi.com)'

'''
Python 3 client SDK for Xiaomi Open API
'''

from XMHttpClient import XMHttpClient
from XMUtils import XMUtils
from urllib.parse import urlparse
import xiaomi_conf

class XMApiClient(XMHttpClient):
    
    def __init__(self, clientId: str, accessToken: str):
        super().__init__(xiaomi_conf.API_URL)
        self.clientId = clientId
        self.accessToken = accessToken
        self.xmUtils = XMUtils()
        self.host = urlparse(xiaomi_conf.API_URL).hostname
        if not self.host:
            raise ValueError(f"Invalid API_URL in configuration: {xiaomi_conf.API_URL}")
    
    def callApi(self, path: str, params: dict, headers: dict = {}, method: str = 'GET') -> dict:
        if not self.url:
            raise ValueError(f"Open API URL error: {self.url}")
        
        res = self.request(path, method, params, headers)
        return self.safeJsonLoad(res.read())
    
    def callApiSelfSign(self, path: str, params: dict, macKey: str, method: str = 'GET') -> dict:
        if params is None:
            params = {}
        
        if 'clientId' not in params:
            params['clientId'] = self.clientId
        if 'token' not in params:
            params['token'] = self.accessToken

        nonce = self.xmUtils.getNonce()
        sign = self.xmUtils.buildSignature(nonce, method, self.host, path, params, macKey)
        headers = self.xmUtils.buildMacRequestHead(self.accessToken, nonce, sign)
        
        return self.callApi(path, params, headers, method)
