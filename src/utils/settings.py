# -*- coding: utf-8 -*-
import os

DEFAULT_SETTINGS_FOLDER = '.box'
DEFAULT_CREDENTIALS_FILE = 'credentials.json'
DEFAULT_SETTINGS_PATH = os.path.join(os.environ.get('HOME'), DEFAULT_SETTINGS_FOLDER)
DEFAULT_CREDENTIALS = os.path.join(DEFAULT_SETTINGS_PATH, DEFAULT_CREDENTIALS_FILE)
DEFAULT_PROMPT = 'Please enter path to credentials:'

def get_credentials(credentials=DEFAULT_CREDENTIALS):
    if os.path.exists(credentials):
        return Settings(credentials)
    credentials = input(DEFAULT_PROMPT)
    return Settings(credentials)

class Settings:
    def __init__(self, credentials=None, *args, **kwargs):
        if not credentials:
            credentials = DEFAULT_CREDENTIALS
        credentials_path, credentials_file= os.path.split(credentials)
        if not os.path.exists(credentials_path):
            os.makedirs(credentials_path, mode=0o775)
        self.path = credentials_path
        self.credentials = credentials
