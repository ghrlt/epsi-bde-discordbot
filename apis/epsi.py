import env

import aiohttp

async def getUserDetails(username: str):
    async with aiohttp.ClientSession() as session:
        async with session.get("%s/%s" % (env.EPSIAPI_USERSURL, username)) as response:
            if response.status == 200:
                return response.status, await response.json()
            else:
                return response.status, None
