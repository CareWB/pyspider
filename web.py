#coding=utf-8

import aiohttp
import asyncio
import async_timeout

file = open("result.txt", 'w+')

async def fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()

async def main(loop):
    async with aiohttp.ClientSession(loop=loop) as session:
        html = await fetch(session, 'http://www.ctrip.com/')
        file.write(html.encode().decode('gbk','ignore'))
        #print(html.encode('utf-8').decode('gbk','ignore'))

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))