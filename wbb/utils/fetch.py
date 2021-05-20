import aiohttp

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}


async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            try:
                data = await resp.json()
            except Exception:
                data = await resp.text()
    return data
