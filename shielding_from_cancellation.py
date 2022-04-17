#!/usr/bin/env python


import asyncio


async def something():
    for _ in range(10):
        print("Doing something...")


async def main():
    await asyncio.shield(something())
    await.sleep(1)
    asyncio.cancel


asyncio.run(main())
