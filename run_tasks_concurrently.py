#!/usr/bin/env python

import asyncio

async def factorial(name: str, number: int) -> int:
    f = 1
    for i in range(2, number + 1):
        print(f"Task {name}: Compute factorial({number}), currently i={i}...")
        await asyncio.sleep(1)
        f *= i
    print(f"Task {name}: factorial({number}) = {f}")
    return f

async def main():
    # Schedule three calls *concurrently*:
    done, pending = await asyncio.wait([
        factorial("A", 2),
        factorial("E", "rashid"),
        factorial("B", 3),
        factorial("C", 4),
    ])
    print(f"These tasks were successfully executed: {done}")



    # looking for tasks that completed with exceptions 
    exceptions = len([task for task in done if 'exception' in str(task)])
    print(f"Number of exceptions: {exceptions}")


asyncio.run(main())
