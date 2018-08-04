# -*- coding: utf-8 -*-

from clients.clients import Client

FAKE_CREDENTIALS_PATH='downloads/fake_jwt.json'

def test_a_client_can_be_created_with_settings():
    client = Client(FAKE_CREDENTIALS_PATH)
    assert client.key.key_size == 2048
