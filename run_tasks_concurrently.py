#!/usr/bin/env python

import asyncio

async def factorial(name: str, number: int) -> int:
    f = 1
    for i in range(2, number + 1):
        print(f"Task {name}: Compute factorial({number}), currently i={i}...")
        await asyncio.sleep(1)
        f *= i
    print(f"Task {name}: factorial({number}) = {f}")

    return (name, number)



async def main():

    # paramters 
    params = [("A", 2), ("E", "rashid"), ({}, {}), ("B", 3), ("C", 4)]


    # awaitables again 
    list_of_awaitables = [factorial(tup[0], tup[1]) for tup in params]


    # Schedule three calls *concurrently*:
    results = await asyncio.gather(*list_of_awaitables, return_exceptions=True)


    # looking for tasks that completed with exceptions 
    output = [result for _, result in zip(list_of_awaitables, results)]

    # tag the results of each coroutine (true for passed and false for failed)
    final_results = [True if isinstance(result, tuple) else False for result in output]

    # get the coroutines that passed
    passed = [params for final_result, params in zip(final_results, params) if final_result == True]

    # get the coroutines that failed 
    failed = [params for final_result, params in zip(final_results, params) if final_result == False]

    # passed coroutines 
    print(passed)

    # failed coroutines 
    print(failed)


asyncio.run(main())
