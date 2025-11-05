import os.path
import time
from threading import Thread
from time import sleep, perf_counter
from typing import Any

from FuncTip import CalculateAny, spiteLine


@CalculateAny
def walk(thread_id: int, sleepTime: int = 0) -> None:
    print(f"starting a walk threading ({thread_id})")
    sleep(sleepTime)
    print(f"walk threading ({thread_id}) is done")


'''
def mutiThread():
    thread_list = []
    for i in range(1, 11):
        t = Thread(target=walk, args=(i,))
        thread_list.append(t)
        t.start()
        #splitLine(f"thread {i} is working")
    for t in thread_list:
        t.join()
    '''


def replaceFile(fileName: str = '', subStr='', new_str='') -> None:
    filePath = os.path.join(os.getcwd(), 'temp', fileName)
    with open(filePath) as f:
        content = f.read()
    content = content.replace(subStr, new_str)
    with open(file=filePath, mode='w+') as f:
        f.writelines(content)
        f.writelines('\n')


def createFile() -> Any:
    return (os.path.join('test_file' + str(chr(64 + i))) for i in range(1, 11))


def main() -> None:
    replFile = [Thread(target=replaceFile, args=(file, 'ol', 'Author')) for file in createFile()]

    for thread_id, thread in enumerate(replFile, start=1):
        print(spiteLine(context=f"the {thread_id} thread is starting"))
        thread.start()
        time.sleep(4)
    for thread_ids, threads in enumerate(replFile, start=1):
        threads.join()
        print(spiteLine(context=f"the {thread_ids} thread is done"))


if __name__ == "__main__":
    print(spiteLine(context="thread thirty,thirty-first is start working"))
    t1Walk = Thread(target=walk(thread_id=30, sleepTime=2))
    t2Walk = Thread(target=walk(thread_id=31, sleepTime=3))
    t1Walk.start()
    t2Walk.start()
    t1Walk.join()
    t2Walk.join()
    print(spiteLine(context="thread thirty,thirty-first is working done"))
    print(spiteLine(context="starting replace the text content work"))
    starTime = perf_counter()
    main()
    endTime = perf_counter()
    print(spiteLine(context=f"it's took {endTime - starTime:.2f} second(s) to compete"))
