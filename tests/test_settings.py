import os
import pytest
import utils.settings as settings

FAKE_CREDENTIALS_PATH='downloads/fake_jwt.json'
BASIC_FAKE_CREDENTIALS_PATH='downloads/basic_fake_jwt.json'
FAKE_PRIVATE_KEY_FILE_PATH='downloads/private.pem'
PASSPHRASE=b'0e0c57a7daf7d0e30672f329b3270447'
def test_full_credentials_file_can_be_read():
    box_settings = settings.Settings(FAKE_CREDENTIALS_PATH)
    with open(FAKE_CREDENTIALS_PATH, 'rb') as fake_file:
        fake_credentials = fake_file.read().decode('utf-8')
    assert box_settings.client_id in fake_credentials
    assert box_settings.client_secret in fake_credentials
    assert box_settings.enterprise_id in fake_credentials
    assert box_settings.public_key_id in fake_credentials
    assert box_settings.webhook_primary_key in fake_credentials
    assert box_settings.webhook_secondary_key in fake_credentials

def test_basic_credentials_file_can_be_read():
    box_settings = settings.Settings(BASIC_FAKE_CREDENTIALS_PATH)
    with open(BASIC_FAKE_CREDENTIALS_PATH, 'rb') as basic_fake_file:
        basic_fake_credentials = basic_fake_file.read().decode('utf-8')
    assert box_settings.client_id in basic_fake_credentials
    assert box_settings.client_secret in basic_fake_credentials
    assert box_settings.enterprise_id in basic_fake_credentials

def test_private_key_file_can_be_read():
    box_settings = settings.Settings(BASIC_FAKE_CREDENTIALS_PATH, 
                                     FAKE_PRIVATE_KEY_FILE_PATH,
                                     passphrase=PASSPHRASE)
    with open(FAKE_CREDENTIALS_PATH, 'rb') as fake_file:
        fake_credentials = fake_file.read().decode('utf-8')
    assert box_settings.client_id in fake_credentials
    assert box_settings.client_secret in fake_credentials
    assert box_settings.enterprise_id in fake_credentials
    assert box_settings.public_key_id in fake_credentials
