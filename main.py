import asyncio
import httpx
from config import settings
from endpoints import endpoints
from pprint import pprint

async def _auth(client: httpx.AsyncClient):
    await client.get(endpoints["mainpage"])
    response = await client.post(endpoints["login"], json={"username": settings._username, "password": settings._password, "application_key": settings._app_key})
    access_token = response.json()
    client.headers.update({"Authorization": f"Bearer {access_token["access_token"]}"})

async def get_user_info(client: httpx.AsyncClient):
    response = await client.get(endpoints["userinfo"])
    return response.json()

async def get_homework(client: httpx.AsyncClient, status: int = 3):
    response = await client.get(f"{endpoints["homework"]}{status}")
    return response.json()

async def main():
    async with httpx.AsyncClient(headers=settings.headers, timeout=30) as client:
        await _auth(client)

asyncio.run(main())