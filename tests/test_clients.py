# -*- coding: utf-8 -*-

from clients.clients import TrioClient, JWTAuth

FAKE_CREDENTIALS_PATH='downloads/fake_jwt.json'

def test_a_client_can_be_created_with_settings():
    jwt_auth = JWTAuth(FAKE_CREDENTIALS_PATH)
    token = jwt_auth.token
    client = TrioClient(token)

