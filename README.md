# async client side rate-limiter

This is some basic code example on how to access the box api with python async calls and rate limiting on the client side.

Since you can easlily reach 10,000 calls a minute with async api calls, you will heavily be rate limited as the rate limit of box is 10 api calls per second, or 600 per minute.

The synchronous strategy of putting in a waiting time won't work with async, as you cannot control a call you already made.

But even for synchrounous calls client side rate limiting is useful as it will increase your overall performance and reduce your cost by eliminating any rate limited calls.

In case of a rate limit, you get a waiting time back, ranging from 3 to 12 seconds. Within this time you could do 30 to 120 calls, an amount you will never be able to catch up to again.

The code implements a token bucket algorithm, rate limiting on your side, and thus avoiding the annoying 429 response code.
