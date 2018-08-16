# -*- coding: utf-8 -*-

from collections import deque

import asks
import json
import string
from pprint import pprint
import trio
import time

DEFAULT_CONNECTIONS = 200
FILE_ENDPOINT = '/files/'
FOLDER_ENDPOINT = '/folders/'

class Client:

    RATE = 10
    MAX_TOKENS = 10

    def __init__(self, auth, connections=DEFAULT_CONNECTIONS, logging=False):
        self.auth = auth
        self.auth.session.headers.update(
            {'Authorization': 'Bearer ' + self.auth.token})
        self.tokens = self.MAX_TOKENS
        self.updated_at = time.monotonic()

    async def get_folder_info(self, folder_id):
        await self.wait_for_token()
        self.auth.session.endpoint = FOLDER_ENDPOINT
        try:
            response = await self.auth.session.get(path=str(folder_id), timeout=60, retries=5)
        except asks.errors.BadHttpResponse:
            response = await self.auth.session.get(path=str(folder_id), timeout=60, retries=5) 
        return response

    async def wait_for_token(self):
        while self.tokens < 1:
            self.add_new_tokens()
            await trio.sleep(1)
        self.tokens -= 1

    def add_new_tokens(self):
        now = time.monotonic()
        time_since_update = now - self.updated_at
        new_tokens = time_since_update * self.RATE
        if new_tokens > 1:
            self.tokens = min(self.tokens + new_tokens, self.MAX_TOKENS)
            self.updated_at = now
