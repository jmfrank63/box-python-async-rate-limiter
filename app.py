# -*- coding: utf-8 -*-
import asks
import csv
import json
import trio

from clients.clients import JWTAuth, TrioClient


async def get_request(domain):
    try:
        response = await session.request('GET', domain, timeout=3)
        print(response.status_code, domain[:-1])
    except:
        pass

        

async def main():
    async with trio.open_nursery() as nursery:
        with open('downloads/domains.txt', 'r') as domain_file:
            for domain in domain_file:
                await trio.sleep(0)
                print(f'{domain[:-1]} added')
                nursery.start_soon(get_request, domain)

if __name__ == '__main__':
    #jwtauth = JWTAuth('downloads/cwe_jwt.json')
    #client = TrioClient('jwtauth.token', requests)
    asks.init('trio')
    session = asks.Session(connections=4000)
    trio.run(main)
