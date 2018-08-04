# -*- coding: utf-8 -*-
import asks
import trio

from clients.clients import JWTAuth, TrioClient

requests = [('GET', 'https://www.box.net'),
            ('GET', 'https://www.google.com'),
            ('GET', 'https://www.debian.org'),
            ('GET', 'https://www.reddit.com'),
            ('GET', 'https://www.t-online.de'),
            ('GET', 'https://www.web.de'),
            ('GET', 'https://www.yahoo.com'),
            ('GET', 'https://www.facebook.com'),
            ('GET', 'https://www.apple.com'),
            ('GET', 'https://www.ubuntu.com')
            ]
if __name__ == '__main__':
    jwtauth = JWTAuth('downloads/cwe_jwt.json')
    client = TrioClient(jwtauth.token, requests)
    print('Done so far!')
    trio.run(client.api_session)
