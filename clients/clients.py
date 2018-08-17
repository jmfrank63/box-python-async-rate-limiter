# -*- coding: utf-8 -*-

from collections import deque

import asks
import json
import string
from pprint import pprint
import trio
import time

API_BASE = 'https://api.box.com/2.0'

DEFAULT_CONNECTIONS = 200

FILE_ENDPOINT = '/files/'
FOLDER_ENDPOINT = '/folders/'

RATE = 10
MAX_TOKENS = 10

class Client:
    def __init__(self, auth, connections=DEFAULT_CONNECTIONS, session=None, rate_limiter=True, rate=RATE, user=None, logging=False):
        self.auth = auth
        if session:
            self.session = session
        else:
            self.session = asks.Session(connections=connections, persist_cookies=True)
        self.session.base_location = API_BASE
        if user:
            self.as_user(user)
        self.session.headers.update(
            {'Authorization': 'Bearer ' + self.auth.token})
        self.rate_limiter(RATE, MAX_TOKENS)
        
    def as_user(self, user_id):
        self.session.headers.update({'As-User' : str(user_id)})

    async def get_folder_info(self, folder_id):
        self.session.endpoint = FOLDER_ENDPOINT
        await self.wait_for_token()
        try:
            response = await self.session.get(path=str(folder_id), timeout=60, retries=5)
        except asks.errors.BadHttpResponse:
            response = await self.session.get(path=str(folder_id), timeout=60, retries=5) 
        return response

    def rate_limiter(self, rate, max_tokens):
        self.tokens = max_tokens
        self.rate = rate
        self.updated_at = time.monotonic()

    async def wait_for_token(self):
        while self.tokens < 1:
            self.add_new_tokens()
            await trio.sleep(1)
        self.tokens -= 1

    def add_new_tokens(self):
        now = time.monotonic()
        time_since_update = now - self.updated_at
        new_tokens = time_since_update * self.rate
        if new_tokens > 1:
            self.tokens = min(self.tokens + new_tokens, self.tokens)
            self.updated_at = now
