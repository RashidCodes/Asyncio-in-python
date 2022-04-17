#!/usr/bin/env python

import asyncio
import time


def blocking_io():
    print(f"start blocking_io at {time.strftime('%X')}")

    # time.sleep could be any IO-bound blocking operation such as file operations
    time.sleep(1)
    print(f"blocking_io complete at {time.strftime('%X')}")



async def main():
    print(f"started main at {time.strftime('%X')}")

    await asyncio.gather(asyncio.to_thread(blocking_io), asyncio.sleep(1))

    print(f"finished main at {time.strftime('%X')}")


asyncio.run(main())
