#!/usr/bin/env python

def blocking_io():
    # File operations (such as logging) can block the event loop
    # Run them in a threadpool
    with open('directory/someFile', 'rb') as f:
        return f.read(100)



def cpu_bound():
    # CPU bound tasks will block the event loop
    return sum(i**2 for i in range(10*5))



async def main():
    loop = asyncio.get_running_loop()

    # 1. Run in the default loop's executor
    result = await loop.run_in_executor(None, blocking_io)

    # 2. Run in a custom threadpool
    with concurrent.futures.ThreadPoolExecutor() as pool:
        result =  await loop.run_in_executor(pool, blocking_io)
        print('Custom thread pool', result)

    # 3. Run in a custom process pool
    with concurrent.futures.ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, cpu_bound)
        print('custom process pool', result)


asyncio.run(main())
