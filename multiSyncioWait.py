import asyncio
import time
from asyncio import FIRST_COMPLETED, Future


class APITimeError(Exception):
    def __init__(self, ansyTask, timeCount: int, message: str):
        self.task = ansyTask
        self.timeCount = timeCount
        self._msg = message

    def __str__(self):
        return self._msg

    @staticmethod
    async def praseError(ansyTask, timeCounter: int):
        taskResult = await asyncio.wait_for(ansyTask, timeout=timeCounter)
        return taskResult


async def CallApi(msg: str, argument, delay: int = 5, raiseError: bool = False, asyncioTask=None):
    print(msg)
    await asyncio.sleep(delay=delay)
    if raiseError:
        raise APITimeError.praseError(ansyTask=asyncioTask, timeCounter=delay)
    else:
        return argument


async def futureTaskCreate(futureIo, argument):
    print(f"creating the future with argument...")
    await asyncio.sleep(1)
    futureIo.set_result(argument)
    return argument


async def futureTaskRun(argument):
    futureTask = Future()
    taskWait = await asyncio.create_task(futureTaskCreate(futureIo=futureTask, argument=argument))
    return taskWait


async def futureTaskEnd(argument):
    asyncFuture = futureTaskRun(argument=argument)
    taskEnd = await asyncFuture
    print(f"future argument is :{taskEnd}")


async def callApiFail(errorMsg: str):
    await asyncio.sleep(delay=1)
    raise APITimeError(None, 1, errorMsg)


async def main():
    task_first = asyncio.create_task(CallApi(msg="Calling api First...", argument=1))
    task_second = asyncio.create_task(CallApi(msg="Calling api second...", argument=2, delay=10))
    task_third = asyncio.create_task(CallApi(msg="Calling api Third...", argument=5,delay=6))
    asyncTuple = (task_first, task_second, task_third)
    taskCounter = 0
    taskSet = set()
    await futureTaskEnd(argument="hello")
    TaskOne, TaskTwo, failInfo = await asyncio.gather(CallApi(msg="Calling api sync First...", argument=4, delay=3),
                                                      CallApi(msg="Calling api sync second...", argument=6, delay=4),
                                                      callApiFail(errorMsg="api calling failing..."),
                                                      return_exceptions=True)
    print(f"the task one result is :{TaskOne}", f"second task is:{TaskTwo}", f"third task is :{failInfo}",
          sep='\n')
    while asyncTuple:
        done, pending = await asyncio.wait(asyncTuple, return_when=FIRST_COMPLETED)
        finishTask = done.pop().result()
        time.sleep(1)
        taskSet.add(finishTask)
        taskCounter += 1
        print(f"response argument is :{finishTask}")
        if taskCounter > 60:
            break
    print(taskSet)


if __name__ == "__main__":
    asyncio.run(main())
