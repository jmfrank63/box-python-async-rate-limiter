# -*- coding: utf-8 -*-

from utils.settings import Settings

from authlib.specs.rfc7519 import jwt

import asks
import json
import random
import string
import time
import trio


AUTH_URL = 'https://api.box.com/oauth2/token'
AUTH_HEADERS =  {'Content-Type': 'application/x-www-form-urlencoded'}

class JWTAuth(Settings):
    def __init__(self, settings_path, alg='RS256', timeout=30, user_id=None):
        super().__init__(settings_path)
        asks.init('trio')
        self.session = asks.Session(connections=200,
                                    persist_cookies=True)
        payload = self.make_payload(alg=alg, timeout=timeout, user_id=user_id)
        trio.run(self.authorize, AUTH_URL, AUTH_HEADERS, payload)

    async def authorize(self, url, headers, payload):
        response = await self.session.post(self.auth_url, headers=headers, data=payload)
        self._access = json.loads(response.content)
        self.valid = int(time.time()) + self._access['expires_in']
        self.token = self._access['access_token']

    def make_payload(self, alg, timeout, user_id):
        self.auth_url = AUTH_URL
        
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
            "aud": self.auth_url,
            "jti": self.random_string(64),
            "exp": exp
        }
        assertion_header = {'alg': alg, 'typ': u'JWT', 'kid': self.public_key_id}

        assertion = jwt.encode(assertion_header, claim, self.key).decode('utf-8')
        return ('grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer'
                '&client_id={}'
                '&client_secret={}'
                '&assertion={}').format(self.client_id, 
                                        self.client_secret, 
                                        assertion)

    def random_string(self, length):
        return ''.join([
            random.choice(string.ascii_letters + string.digits)
            for n in range(length)
        ])