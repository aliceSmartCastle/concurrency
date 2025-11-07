import os.path
from threading import Thread
from typing import List
from urllib.request import urlopen
from FuncTip import CalculateAny, GetterMemory


def DownloaderFile(url: str) -> None:
    print(f"download from the the {url}")
    pngData = None
    with urlopen(url) as Png:
        pngData = Png.read()
    if not pngData:
        raise Exception(f"Error: could not download the image from {url}")
    FileName = os.path.basename(url)
    #PngName, _ = request.urlretrieve(url, FileName)
    #downEvent.set()
    print("Waiting for the PngFile to be downloaded...")
    with open(os.path.join('pjskPng', FileName), 'wb+') as pngFile:
        pngFile.write(pngData)
        print(f"{FileName} is download...")
    print("file download is competed")
    #downEvent.wait()


@CalculateAny
# its Decorators can calculate all thread download of time
def main(urls: List[str]) -> None:
    """
    the Thread Event and Lock is not needs,so use the '#' to comment it
    """

    if urls:
        #pngLock = Lock()

        # PngThread = Thread(target=DownloaderFile, args=(urls[0], pngEvent))
        multiThreadDownload = (Thread(target=DownloaderFile, args=(urls[i],)) for i in range(len(urls)))
        finish_list = []
        for pngThread in multiThreadDownload:
            finish_list.append(pngThread)
            pngThread.start()
        for pngFinish in finish_list:
            pngFinish.join()
            print(f"all thread download picture successfully")
        GetterMemory()
        # watch the download codes use tge rss and vss
    else:
        print('not support empty list')


if __name__ == "__main__":
    urlList = ['https://wallpapercave.com/wp/wp11393211.png',
               'https://wallpapercave.com/wp/wp12211568.jpg']
    main(urls=urlList)
