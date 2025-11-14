import asyncio
import math
import time
from asyncio import CancelledError
from typing import Any


async def squareApi(msg: str, result: int = 100, delay: int = 5):
    print(msg)
    await asyncio.sleep(delay)
    return result


async def square(basic: float, top: float) -> float:
    return math.pow(basic, top)


async def squareCalculate(basicTop):
    def noNative(num: float) -> float:

        if num < 0:
            return abs(num)
        elif num == 0:
            nums = 2
            return nums
        else:
            return num

    squareFirst = await square(basic=noNative(num=basicTop), top=noNative(num=basicTop + 1))
    squareSecond = await square(basic=noNative(num=basicTop), top=noNative(num=basicTop - 1))
    if squareFirst == squareSecond:
        return squareFirst
    else:
        differenceVal = max([squareSecond, squareFirst]) - min([squareFirst, squareSecond])
        return round(differenceVal, 4)


async def sleepIo():
    for _ in range(5):
        await asyncio.sleep(1)
        print(f"spareAqi call in process...")


async def asyncHandle(taskList, time_elapsed: int = 0):
    for task in taskList:
        if task.done():
            return task
        while not task.done():
            time_elapsed += 1
            await asyncio.sleep(1)
            print(f"task is not await finish,please waiting the some seconds")
            if time_elapsed > 10:
                print("cancelling the task...")
                task.cancel()
                break
        else:
            return task
    return None


async def taskSpendTime(taskList, timeErrorCount: int = 1):
    for task in taskList:
        print(f"watch task spend time...")
        await asyncio.wait_for(asyncio.shield(task), timeout=timeErrorCount)
    else:
        return ''


async def main() -> Any:
    squareStart = time.perf_counter()
    bigNumber = await squareCalculate(basicTop=4)
    smallNumber = await squareCalculate(basicTop=3)
    squareTask = asyncio.create_task(sleepIo())
    try:

        processNumber = asyncio.create_task(squareApi(msg="the difference bigger value is... ", result=bigNumber))
        processSpare = asyncio.create_task(squareApi(msg="the difference small value is...", result=smallNumber))
        squareNumber = await processNumber
        print(f"big spare number is :{squareNumber}")
        smallNumber = await processSpare
        print(f"small spare number is:{smallNumber}")
        await asyncHandle(taskList=[processNumber, processSpare, squareTask])
        await taskSpendTime(taskList=[processNumber, processSpare, squareTask])

    except (CancelledError, TimeoutError) as e:
        print(e)

    squareEnd = time.perf_counter()
    print(f'It took {round(squareEnd - squareStart, 6)} second(s) to complete.')


if __name__ == "__main__":
    asyncio.run(main(), debug=True)
