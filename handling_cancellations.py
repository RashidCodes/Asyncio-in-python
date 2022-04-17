#!/usr/bin/env python


import asyncio

async def cancel_me():
    print("cancel_me(): before sleep")

    try:
        print("Sleeping in peace")
        await asyncio.sleep(5)
    except asyncio.CancelledError:
        print("cancel_me(): cancel sleep")
        raise
    finally:
        print("cancel_me(): after sleep")


async def main():
    # Create a cancel me task
    task = asyncio.create_task(cancel_me())

    # wait for one second
    await asyncio.sleep(1)

    # cancel the task that contains the cancel_me coroutine. This will raise a asyncio.CancelledError exception in the coroutine. We gracefully handle this exception though.
    task.cancel()

    try:
        await task # task has been cancelled so an asyncio.CancelledError exception is raised
    except:
        print("main(): cancel_me is cancelled now")



asyncio.run(main())
