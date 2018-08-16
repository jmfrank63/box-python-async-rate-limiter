# -*- coding: utf-8 -*-
import json
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import dsa, rsa
from cryptography.hazmat.primitives.serialization import load_pem_private_key

DEFAULT_SETTINGS_FOLDER_NAME = '.box'
DEFAULT_CREDENTIALS_FILE_NAME = 'credentials.json'
DEFAULT_PRIVATE_KEY_FILE_NAME = 'private.pem'
try:
    DEFAULT_SETTINGS_FOLDER_PATH = os.path.join(os.environ['HOMEPATH'], DEFAULT_SETTINGS_FOLDER_NAME)
except KeyError:
    DEFAULT_SETTINGS_FOLDER_PATH = os.path.join(os.environ['HOME'], DEFAULT_SETTINGS_FOLDER_NAME)
DEFAULT_CREDENTIALS_FILE_PATH = os.path.join(DEFAULT_SETTINGS_FOLDER_PATH, DEFAULT_CREDENTIALS_FILE_NAME)
DEFAULT_PRIVATE_KEY_FILE_PATH = os.path.join(DEFAULT_SETTINGS_FOLDER_PATH, DEFAULT_PRIVATE_KEY_FILE_NAME)


class Settings:
    def __init__(self, credentials_file_path=DEFAULT_CREDENTIALS_FILE_PATH, 
                 privat_key_file_path=DEFAULT_PRIVATE_KEY_FILE_PATH,
                 passphrase=None):
        self.credentials_file_path = credentials_file_path
        with open(self.credentials_file_path, 'rb') as credentials_file:
            self.credentials = json.loads(credentials_file.read())

        self.client_id = self.credentials['boxAppSettings']['clientID']
        self.client_secret = self.credentials['boxAppSettings']['clientSecret']
        self.enterprise_id = self.credentials['enterpriseID']

        if self.credentials['boxAppSettings']['appAuth']['publicKeyID']:
            self.public_key_id = self.credentials['boxAppSettings']['appAuth']['publicKeyID']
            _private_key = self.credentials['boxAppSettings']['appAuth']['privateKey'].encode('utf-8')
            _passphrase = self.credentials['boxAppSettings']['appAuth']['passphrase'].encode('utf-8')
            self.key = load_pem_private_key(_private_key, _passphrase, default_backend())

        if os.path.exists(privat_key_file_path):
            self.public_key_id = self.credentials['boxAppSettings']['appAuth']['publicKeyID']
            with open(privat_key_file_path, 'rb') as private_key_file:
                _private_key = private_key_file.read()
                _passphrase = passphrase
            self.key = load_pem_private_key(_private_key, _passphrase, default_backend())

        if 'webhooks' in self.credentials:
            self.webhook_primary_key = self.credentials['webhooks']['primaryKey']
            self.webhook_secondary_key = self.credentials['webhooks']['secondaryKey']
