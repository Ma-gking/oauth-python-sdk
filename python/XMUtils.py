#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
__author__ = 'xiaomi passport (xiaomi-account-dev@xiaomi.com)'

'''
Python 3 client SDK utility for Xiaomi Open API
'''

import random
import sys
import time
import hmac
import hashlib
import base64
from urllib.parse import quote


class XMUtils:
    '''
    Utility functions for generating nonce, MAC signature, and headers
    '''

    def getNonce(self) -> str:
        r = random.randint(-sys.maxsize, sys.maxsize)
        m = int(time.time() / 60)
        return f"{r}:{m}"

    def getSignString(self, nonce: str, method: str, host: str, path: str, params: dict) -> str:
        if not nonce or ':' not in nonce:
            raise ValueError(f"Invalid nonce: {nonce}")
        if method not in ('GET', 'POST') or not host:
            raise ValueError("Invalid method or host")

        sign = [nonce, method.upper(), host, path or ""]

        sorted_keys = sorted(params.keys()) if params else []
        items = [f"{key}={params[key]}" for key in sorted_keys]

        sign.append('&'.join(items) if items else '')
        return '\n'.join(sign) + '\n'

    def buildSignature(self, nonce: str, method: str, host: str, path: str, params: dict, secret: str) -> str:
        signString = self.getSignString(nonce, method, host, path, params)
        h = hmac.new(secret.encode('utf-8'), signString.encode('utf-8'), hashlib.sha1)
        signature = base64.b64encode(h.digest()).decode('utf-8').strip()
        return signature

    def buildMacRequestHead(self, accessToken: str, nonce: str, sign: str) -> dict:
        macHeader = f'MAC access_token="{quote(accessToken)}", nonce="{nonce}", mac="{quote(sign)}"'
        return {'Authorization': macHeader}
