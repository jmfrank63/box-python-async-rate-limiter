# -*- coding: utf-8 -*-

from auth.jwt_auth import JWTAuth
from clients.clients import Client
from collections import deque

import asks
import datetime
import json
import trio
import timeit
import time
import os

API_BASE = 'https://api.box.com/2.0'

FOLDER =  50245725082

folders = {}

async def get_folders(folder_id, nursery):
        async def add_children(response):
            content = json.loads(response.content)
            child_folders = []
            for entry in content['item_collection']['entries']:
                await trio.sleep(0)
                if entry['type'] == 'folder':
                    folder = int(entry['id'])
                    child_folders.append(folder)
                    nursery.start_soon(get_folders, folder, nursery)
            print(folder_id, child_folders)
            folders[folder_id] = child_folders

        response = await client.get_folder_info(folder_id)
        if response.status_code == 200:
            await add_children(response)
        elif response.status_code == 429:
            while response.status_code == 429:
                wait = int(response.headers['Retry-After'])
                await trio.sleep(int(wait))
                await add_children(response)

async def get_folder_tree(nursery, folder):
    nursery.start_soon(get_folders, folder, nursery)

async def main():
    async with trio.open_nursery() as nursery:
        nursery.start_soon(get_folder_tree, nursery, FOLDER)
    
if __name__ == '__main__':
    jwt_auth = JWTAuth(os.path.join('downloads','cwe_jwt.json'))
    client = Client(jwt_auth)
    client.auth.session.base_location = API_BASE
    client.auth.session.headers.update({'As-User' : '1827788631'})
    trio.run(main)
    print(folders)
