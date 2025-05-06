#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
__author__ = 'xiaomi passport (xiaomi-account-dev@xiaomi.com)'

'''
Python 3 client SDK for Xiaomi Open API - OAuth2 Client
'''

from XMHttpClient import XMHttpClient
import xiaomi_conf
from urllib.parse import urljoin

class XMOAuthClient(XMHttpClient):
    
    OAUTH2_PATH = {
        'authorize': '/oauth2/authorize',
        'token': '/oauth2/token'
    }

    def __init__(self, clientId: str, clientSecret: str, redirectUri: str):
        super().__init__(xiaomi_conf.OAUTH2_URL)
        self.clientId = clientId
        self.clientSecret = clientSecret
        self.redirectUri = redirectUri

    def getAuthorizeEndpoint(self) -> str:
        if not self.url:
            raise ValueError(f"Invalid OAuth URL: {self.url}")
        return urljoin(self.url, self.OAUTH2_PATH['authorize'])

    def getTokenEndpoint(self) -> str:
        if not self.url:
            raise ValueError(f"Invalid OAuth URL: {self.url}")
        return urljoin(self.url, self.OAUTH2_PATH['token'])

    def getAuthorizeUrl(
        self,
        responseType: str = 'code',
        display: str = '',
        state: str = '',
        scope: list = []
    ) -> str:
        params = {
            'client_id': self.clientId,
            'response_type': responseType,
            'redirect_uri': self.redirectUri
        }

        if display:
            params['display'] = display
        if scope:
            params['scope'] = ' '.join(scope).strip()
        if state:
            params['state'] = state

        return self.getAuthorizeEndpoint() + '?' + self.buildQueryString(params)

    def getAccessTokenByAuthorizationCode(self, code: str) -> dict:
        params = {
            'client_id': self.clientId,
            'client_secret': self.clientSecret,
            'redirect_uri': self.redirectUri,
            'grant_type': 'authorization_code',
            'code': code,
            'token_type': 'mac'
        }
        return self.getAccessToken(params)

    def getAccessTokenByRefreshToken(self, refreshToken: str) -> dict:
        params = {
            'client_id': self.clientId,
            'client_secret': self.clientSecret,
            'redirect_uri': self.redirectUri,
            'grant_type': 'refresh_token',
            'refresh_token': refreshToken,
            'token_type': 'mac'
        }
        return self.getAccessToken(params)

    def getAccessToken(self, params: dict) -> dict:
        res = self.get(self.OAUTH2_PATH['token'], params)
        return self.safeJsonLoad(res.read())
