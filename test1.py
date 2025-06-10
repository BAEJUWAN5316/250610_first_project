import httpx

async def fetch_gpt():
    async with httpx.AsyncClient() as client:
        res = await client.post("https://gpt-api.com", json={"key": "value"})
        print(res.json())