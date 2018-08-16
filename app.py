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

API_BASE = 'https://api.box.com/2.0'
RATE = 10

# {'type': 'folder', 'id': '46253564892', 'sequence_id': '0', 'etag': '0', 'name': 'Admin'}
# {'type': 'folder', 'id': '50761640896', 'sequence_id': '0', 'etag': '0', 'name': 'Backup'}
# {'type': 'folder', 'id': '28909612557', 'sequence_id': '0', 'etag': '0', 'name': 'Box Notes Images'}
# {'type': 'folder', 'id': '33265476567', 'sequence_id': '0', 'etag': '0', 'name': 'Box Reports'}
# {'type': 'folder', 'id': '50245725082', 'sequence_id': '0', 'etag': '0', 'name': 'DevVMBackup'}
# {'type': 'folder', 'id': '43848385007', 'sequence_id': '0', 'etag': '0', 'name': 'Example Files'}
# {'type': 'folder', 'id': '52325253875', 'sequence_id': '0', 'etag': '0', 'name': 'Gallery'}
# {'type': 'folder', 'id': '50431672757', 'sequence_id': '0', 'etag': '0', 'name': 'Gmail Attachments'}
# {'type': 'folder', 'id': '43848319953', 'sequence_id': '0', 'etag': '0', 'name': 'jmfrank63@gmail.com'}
# {'type': 'folder', 'id': '31820709870', 'sequence_id': '3', 'etag': '3', 'name': 'jmfrank@common-work-education.co.uk'}
# {'type': 'folder', 'id': '28909418112', 'sequence_id': '0', 'etag': '0', 'name': 'My Box Notes'}
# {'type': 'folder', 'id': '50790640207', 'sequence_id': '0', 'etag': '0', 'name': 'Software'}
# {'type': 'folder', 'id': '48802152954', 'sequence_id': '0', 'etag': '0', 'name': 'SSC Scan Archive'}
# {'type': 'folder', 'id': '51337972463', 'sequence_id': '0', 'etag': '0', 'name': 'Tests'}

FOLDER =  50245725082 #52325253875

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
    jwt_auth = JWTAuth('downloads/cwe_jwt.json')
    client = Client(jwt_auth)
    client.auth.session.base_location = API_BASE
    client.auth.session.headers.update({'As-User' : '1827788631'})
    trio.run(main)
    print(folders)
