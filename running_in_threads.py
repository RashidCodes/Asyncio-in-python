#!/usr/bin/env python


import asyncio
import time


def blocking_io():
	print(f"start blocking_io at {time.strftime('%X')}")
	time.sleep(1)
	print(f"blocking_io complete at {time.strftime('%X')}")


def another_blocking_io():
    print(f"start another blocking_io at {time.strftime('%X')}")
    time.sleep(3)
    print(f"another blocking_io complete at {time.strftime('%X')}")


async def main():
	print(f"started main at {time.strftime('%X')}")

	await asyncio.gather(asyncio.to_thread(blocking_io), asyncio.sleep(1), asyncio.to_thread(another_blocking_io))

	print(f"finished main at {time.strftime('%X')}")


asyncio.run(main())


