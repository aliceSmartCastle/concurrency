import http.client
from typing import List, Any
from urllib.error import URLError
from urllib.request import urlopen
from urllib import error
from threading import Thread
from FuncTip import CalculateAny, spiteLine


class NetworkThread(Thread):
    def __init__(self, urlAddress: str = ''):
        super().__init__()
        self.httStateCode = 0
        self.httReason = URLError(reason='')
        self.address = urlAddress
        self.extraError = None
        self.addressList:List[Any] = []
        self.stateCodeList:List[Any] = []
        self.reasonList:List[Any] = []

    def addressNull(self, address) -> None:
        if self.address:
            self.addressList.append(self.address)
        else:
            self.address = "empty address"
            self.addressList.append(address)

    @staticmethod
    def reasonNull(reason) -> list:
        if reason:
            ...
        else:
            reason = ['ok']
        return reason

    def run(self) -> None:
        try:
            response = urlopen(self.address)
            self.addressList.append(self.address)
            self.httStateCode = response.code
            if self.httStateCode == 200:
                print(f"{self.address} is connect successfully")
                self.stateCodeList.append(self.httStateCode)
        except error.HTTPError as err:
            self.httStateCode = err.code
            self.addressNull(address=self.address)
            self.stateCodeList.append(self.httStateCode)
            self.reasonList.append(err.reason)
            print(f"{self.address} is connecting during HttpError")
        except error.URLError as urlErr:
            self.httReason = urlErr
            print(f"{self.address} is connecting during urlError")
            self.addressNull(address=self.address)
            self.stateCodeList.append(None)
            self.reasonList.append(self.httReason)
        except http.client.RemoteDisconnected as httErr:
            httErr.errno = self.extraError
            print(f"{self.address} is connecting during extraError")
            self.addressNull(address=self.address)
            self.stateCodeList.append(self.extraError)


        # print(dict(zip(tuple(zip(self.addressList,self.stateCodeList)),self.reasonNull(self.reasonList))))
        finalInfo = tuple(zip(self.addressList, self.stateCodeList, self.reasonNull(self.reasonList)))
        print(finalInfo[0])

@CalculateAny
def main():
    url = [
        'https://github.com',
        'https://www.python.org',
        'https://www.baidu.com',
        'https://www.google.com',
        'https://www.bilibili.com',
        'https://www.zhihu.com',
    ]
    httpsInfo = (NetworkThread(urlAddress) for urlAddress in url)

    for ids, connect in enumerate(httpsInfo, start=1):
        print(spiteLine(context='the {} thread is starting'.format(ids)))
        connect.start()
        print(spiteLine(context='the {} thread is ending'.format(ids)))
        connect.join()


if __name__ == '__main__':
    main()
