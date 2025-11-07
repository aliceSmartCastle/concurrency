import time
from threading import Thread
from FuncTip import CalculateAny


class numericalCalc(Thread):
    def __init__(self, daemons, first, second):
        super().__init__(daemon=daemons)
        self.fst = first
        self.snd = second

    def add(self):
        return self.fst + self.snd

    def sub(self):
        return self.fst - self.snd

    def mul(self):
        return self.fst * self.snd

    def div(self):
        return round(self.fst / self.snd, 4)

    @staticmethod
    def waitingTime():
        count = 0
        question = input("Do you want to exit?\n")
        while True:
            count += 15

            print(f"you are waiting for {count} seconds(s)...")
            if count > 30 or question.lower() == 'y':
                break

    def run(self):
        print(f"add: {self.fst}+{self.snd}={self.add()}")
        print(f"sub: {self.fst}-{self.snd}={self.sub()}")
        print(f"mul: {self.fst}*{self.snd}={self.mul()}")
        print(f"div: {self.fst}/{self.snd}={self.div()}")
        print(f"one thread calculate finish\n")
        self.waitingTime()


@CalculateAny
def main():
    numbersList = [(i, i + 3) for i in range(20, 25)]

    endPool = []
    for calculate in numbersList:
        num = numericalCalc(first=calculate[0], second=calculate[1], daemons=True)
        endPool.append(num)
        num.start()
    for endPro in endPool:
        endPro.join()


if __name__ == "__main__":
    main()
