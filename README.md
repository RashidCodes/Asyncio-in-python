# Learning about async/await in Python

## Coroutines
Coroutines are implemeted with the **async def** statement.

```python
import asyncio

async def main():
	print('hello')
	await asyncio.sleep(1)
	print('world')
```

A coroutine can be run using three main mechanisms namely:
- ```asyncio.run()```
- ```Awaiting``` on a coroutine
- ```asyncio.create_task()```

<blockquote>Note that calling the <code>main()</code> function will not schedule the coroutine to run.</blockquote>

<br/>

### <code>asyncio.run()</code>
This function is used to run coroutines. It takes care of the asyncio event loop, *finalises asynchronous generators*, and closes the threadpool.

```asyncio.run()``` cannot be run while another ```asyncio``` event loop is running in the same thread.

<blockquote>In computer science, the event loop is a programming construct or design pattern that waits for and dispatches events or messages in a program. </blockquote>

<br/>

### <code>Awaiting</code> on a coroutine
It's simply used to wait on the execution of a coroutine.

<br/>

### <code>asyncio.create_task()</code>
This function is used to encapsulate a coroutine into a ```Task``` and schedule its execution. It returns a ```Task``` object.

```python

async def main():
	task1 = asyncio.create_task(say_after(1, 'hello'))
	task2 = asyncio.create_task(say_after(2, 'world'))

	print(f"started at {time.strftime('%X')}")

	# wait on the completion of both tasks
	await task1
	await task2

	print(f"finished at {time.strftime('%X')}")

asyncio.run(main())
```

<br/>


## Awaitables
An object is awaitable if it can be used with an <code>await</code> expression. The three main types of awaitables are:
- coroutines
- Tasks
- Futures


```python
import asyncio

async def nested():
	return 42

async def main():
	# A coroutine object is created 
	# But nothing happens because it's not awaited
	nested() 

	# Let's await now 
	print(await nested())


```

<br/>

## Sleeping with <code>asyncio.sleep(<i>delay, result=None</i>)</code>
Sleeping is blocking an operation for a few seconds. A result is provided to the caller when a coroutine completes. To allow for long-running functions to avoid hogging up the event loop while they execute, the delay can be set to 0 to provide an optimized path to allow other tasks to run.


```python
import asyncio
import datetime


async def display_date():
	loop = asyncio.get_running_loop()
	end_time = loop.time() + 5.0
	while True:
		print(datetime.datetime.now())
		if (loop.time() + 1.0) >= end_time:
			break
		await asyncio.sleep(1) # sleep

asyncio.run(display_date())
```

<br/>

## Running tasks concurrently using <code>asyncio.gather(<i>\*aws, return_exceptions=False</i>)</code>

If any awaitable in <i>aws</i> is a coroutine, it is automatically scheduled as a ```Task```.

If all awaitables execute successfully, each result is persisted in a list. The order of this list corresponds to the order of the awaitables in *aws*.

Some awaitables may return errors. If *return_exceptions* is set False (default), the exception raised is propagated to the taskthat awaits on ```gather()```.

```python

#!/usr/bin/env python

import asyncio

async def factorial(name, number):
    f = 1
    for i in range(2, number + 1):
        print(f"Task {name}: Compute factorial({number}), currently i={i}...")
        await asyncio.sleep(1)
        f *= i
    print(f"Task {name}: factorial({number}) = {f}")
    return f

async def main():
    # Schedule three calls *concurrently*:
    L = await asyncio.gather(
        factorial("A", 2),
        factorial("E", "rashid"), # return an error
        factorial("B", 3),
        factorial("C", 4),

	# exceptions are treated the same as successful results, and aggregated in the result list.
        return_exceptions=True
    )
    print(L)


asyncio.run(main())

```

<br/>

## Shielding from cancellation using <code>asyncio.shield(<i>aw</i>)</code>

You can protect a coroutine from being cancelled using ```asyncio.shield```.

<b>If <i>aw</i> is a coroutine then it is automatically scheduled as a task</b>

The statement:
```python
res = await shield(something())
``` 

is similar to 
```python
res = await something()
```

unless the scheduled task is cancelled. In that case, ```something()``` keeps running but it raises a <code>asyncio.CancelledError</code>.

If you wanted to completely ignore cancellation, then you can use the try/except clause as follows (see [handling_cancellations](https://github.com/RashidCodes/Asyncio-in-python/blob/main/handling_cancellations.py)):
```python
try:
	res = await shield(something())
except CancelledError:
	res = None
```

This practice however is not recommended.


<br/>


## Timeouts with <code>asyncio.wait_for(<i>aw, timeout</i>)</code>
```python
async def eternity():
	# Sleep for eternity
	await asyncio.sleep(3600)
	
	print("Can you sleep longer than this?")


async def main():
	try:
		await asyncio.wait_for(eternity(), timeout=1.0)
	except asyncio.TimeoutError:
		print('timeout!')


asyncio.run(main())
```


<br/>

## Running in Threads with <code>asyncio.to_thread(<i>func, /, \*\*args, \*\*\*kwargs)</i>)</code>

If you have several blocking IO bound tasks, you can run them in different threads using ```asyncio``` as follows. An interesting thing to remember here is <code>asyncio.gather()</code>. Even though you're running several blocking IO operations in different threads, the awaitables are still run in a specific sequence.

```python
def blocking_io():
	print(f"start blocking_io at {time.strftime('%X')}")
	time.sleep(1)
	print(f"blocking_io complete at {time.strftime('%X')}")



async def main():
	print(f"started main at {time.strftime('%X')}")

	await asyncio.gather(asyncio.to_thread(blocking_io), asyncio.sleep(1))

	print(f"finished main at {time.strftime('%X')}")


asyncio.run(main())

```

<br/>

## Executing code in thread or process pools with asyncio
You can executor blocking or cpu-bound operations in thread or process pools (executors).

```python

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
    with concurrent.futures.ThreadPoolExecutor() as executor:
        result =  await loop.run_in_executor(executor, blocking_io)
        print('Custom thread pool', result)

    # 3. Run in a custom process pool
    with concurrent.futures.ProcessPoolExecutor() as executor:
        result = await loop.run_in_executor(executor, cpu_bound)
        print('custom process pool', result)


asyncio.run(main())

```

<br/>


# References:
[Asyncio](https://docs.python.org/3/library/asyncio.html)

