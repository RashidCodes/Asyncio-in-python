#!/usr/bin/env python

import asyncio


async def factorial(name: str, number: int) -> int:

    f = 1

    for i in range(2, number + 1):
        print(f"Task {name}: Compute factorial({number}), currently i={i}...")


        try:
            f *= i
        except TypeError:
            rashid = "failure"
        else:
            rashid = "success"
            print(f"Task {name}: factorial({number}) = {f}")
            return(name, number,"passed")
        finally:
            if rashid == "failure":
                return "show me that you're the boss"
            return "some error occurred"



def handle_exception(loop, context):
    msg = context.get("exception", context["message"])
    logging.error(f"Caugh exception: {msg}")



async def main():

    loop = asyncio.get_event_loop()

    

    # paramters 
    params = [("A", 2), ("E", "rashid"), ({}, {}), ("B", 3), ("C", 4)]


    # awaitables again 
    list_of_awaitables = [factorial(tup[0], tup[1]) for tup in params]


    # Schedule three calls *concurrently*:
    try:
        results = await asyncio.gather(*list_of_awaitables, return_exceptions=True)

    except BaseException as err:
        print('something was excepted')
        print(err)

    else:
        print("something was not excepted")
        print(results)

    finally:
        # this block will always run
        print ("ha")


    loop.set_exception_handler(handle_exception)


asyncio.run(main())
