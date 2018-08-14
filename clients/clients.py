# -*- coding: utf-8 -*-
from utils.settings import Settings
from asks import Session
from collections import deque

import asks
import curio
import json
import requests
import random
import string
import time
import trio

from authlib.specs.rfc7519 import jwt


class TrioClient:
    def __init__(self, token, nursery, connections=10000, logging=False):
        asks.init('trio')
        self.token = token
        self.session = asks.Session(
            connections=connections,
            headers={f'Authorization bearer: {self.token}'})

    async def request(self, method, url):
        try:
            response = await self.session.request(method, url, timeout=5)
            print(f'Got response {response.status_code} from {url}')
            return response.status_code
        except (asks.errors.AsksException, OSError, trio.BrokenStreamError,
                ValueError, KeyError) as exp:
            print(f'Ignoring call to {url} because of {exp}')


class JWTAuth(Settings):
    def __init__(self, settings_path, alg='RS256', timeout=30, user_id=None):
        super().__init__(settings_path)
        self.url = 'https://api.box.com/oauth2/token'
        self.header = {'alg': alg, 'typ': u'JWT', 'kid': self.public_key_id}
        if user_id:
            sub = user_id
            sub_type = 'user'
        else:
            sub = self.enterprise_id
            sub_type = 'enterprise'
        exp = int(time.time()) + timeout
        claim = {
            "iss": self.client_id,
            "sub": sub,
            "box_sub_type": sub_type,
            "aud": self.url,
            "jti": self.random_string(64),
            "exp": exp
        }
        assertion = jwt.encode(self.header, claim, self.key).decode('utf-8')
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = 'grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer&\
client_id={}&client_secret={}&assertion={}'\
                   .format(self.client_id, self.client_secret, assertion)
        response = requests.post(self.url, headers=headers, data=payload)
        self.access = json.loads(response.content)
        self.valid = int(time.time()) + self.access['expires_in']
        self.token = self.access['access_token']

    def random_string(self, length):
        return ''.join([
            random.choice(string.ascii_letters + string.digits)
            for n in range(length)
        ])
