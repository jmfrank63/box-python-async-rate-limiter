# -*- coding: utf-8 -*-
from utils.settings import Settings, jti
from asks import Session
from collections import deque

import asks
import curio
import json
import requests
import time
import trio

from authlib.specs.rfc7519 import jwt

class RequestQueue(deque):
    def __init__(self, elements):
        super().__init__(elements)
    def __aiter__(self):
        return self
    async def __anext__(self):
        if not self:
            await self._get_elements()
            if not self:
                raise StopAsyncIteration
        element, args = self.popleft()
        return element, args

    async def _get_elements(self):
        elements = await asks.get('https://www.gentoo.org')
        self.extend(elements)

class TrioClient:
    def __init__(self, token, requests, logging=False):
        self.token = token
        self.requests = RequestQueue(requests)
        self.results = []
        asks.init('trio')

    async def api_session(self):
        self.session = asks.Session()
        async with trio.open_nursery() as session_nursery: # pylint: disable=no-member
            session_nursery.start_soon(self.request_loop)
            
    async def request_loop(self):
        async with trio.open_nursery() as requests_nursery: # pylint: disable=no-member
            async for method, args in self.requests:
                print('Making request to {}'.format(args))
                requests_nursery.start_soon(self.make_request, method, args)

    async def make_request(self, method, args):
        response = await self.session.request(method, args)
        print('Got {} from {}'.format(response.status_code, args))
        self.results.append(response)
    
class JWTAuth(Settings):
    def __init__(self, settings_path, alg='RS256', timeout=30, user_id=None):
        super().__init__(settings_path)
        self.url = 'https://api.box.com/oauth2/token'
        self.header = { 'alg': alg, 'typ': u'JWT', 'kid': self.public_key_id}
        if user_id:
            sub = user_id
            sub_type = 'user'
        else:
            sub = self.enterprise_id
            sub_type = 'enterprise'
        exp = int(time.time()) + timeout
        claim = { "iss": self.client_id,
                                "sub": sub,
                                "box_sub_type": sub_type,
                                "aud": self.url,
                                "jti": jti(64),
                                "exp": exp }
        assertion = jwt.encode(self.header, claim, self.key).decode('utf-8')
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = 'grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer&\
client_id={}&client_secret={}&assertion={}'\
                   .format(self.client_id, self.client_secret, assertion)
        response = requests.post(self.url, headers=headers, data=payload)
        self.access = json.loads(response.content)
        self.valid = int(time.time()) + self.access['expires_in']
        self.token = self.access['access_token']
