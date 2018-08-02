# -*- coding: utf-8 -*-
import json
import os

DEFAULT_SETTINGS_FOLDER_NAME = '.box'
DEFAULT_CREDENTIALS_FILE_NAME = 'credentials.json'
DEFAULT_SETTINGS_FOLDER_PATH = os.path.join(os.environ.get('HOME'), DEFAULT_SETTINGS_FOLDER_NAME)
DEFAULT_CREDENTIALS_FILE_PATH = os.path.join(DEFAULT_SETTINGS_FOLDER_PATH, DEFAULT_CREDENTIALS_FILE_NAME)

class Settings:
    def __init__(self, credentials_file_path=DEFAULT_CREDENTIALS_FILE_PATH):
        self.credentials_file_path = credentials_file_path
        with open(self.credentials_file_path, 'r') as credentials_file:
            self.credentials = json.loads(credentials_file.read().replace('\n', ''))
        self.client_id = self.credentials['boxAppSettings']['clientID']
        self.client_secret = self.credentials['boxAppSettings']['clientSecret']
        self.enterprise_id = self.credentials['enterpriseID']
        self.public_key_id = self.credentials['boxAppSettings']['appAuth']['publicKeyID']
        self.private_key = self.credentials['boxAppSettings']['appAuth']['privateKey']
        self.passphrase = self.credentials['boxAppSettings']['appAuth']['passphrase']
        if 'webhooks' in self.credentials:
            self.webhook_primary_key = self.credentials['webhooks']['primaryKey']
            self.webhook_secondary_key = self.credentials['webhooks']['secondaryKey']
