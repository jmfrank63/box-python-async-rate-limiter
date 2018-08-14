# -*- coding: utf-8 -*-

import trio
import asks
import timeit

asks.init('trio')

results = []

async def grabber(domain):
    try:
        r = await session.request(*domain, timeout=3)
        results.append((domain[1], r.status_code))
        #print(f'Got status {r.status_code} for {domain[1]}')
    except:
        pass
        #print(f'Domain {domain[1]} skipped')

async def gen(nursery):
    async with await trio.open_file('downloads/domains.txt') as domain_file:
        idx = 0
        async for domain in domain_file:
            #print(f'{idx} Domain {domain[:-1]} added for request...')
            nursery.start_soon(grabber, ('GET', domain[:-1]))
            idx += 1

async def main():
    async with trio.open_nursery() as nursery:
        await gen(nursery)

if __name__ == '__main__':
    session = asks.Session(connections=2000)
    start = timeit.default_timer()
    trio.run(main)
    stop = timeit.default_timer()
    print(len(results))
    print(stop - start)