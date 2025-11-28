import os.path
import random
import time
import typing
import urllib.error
from threading import Thread
from typing import List, Optional
import requests
from typing_extensions import Annotated
import typer
from FuncTip import CalculateAny, GetterMemory
from typing import Literal
from time import perf_counter

aqq = typer.Typer()


def pictureBar():
    for loading in range(100):
        yield loading


def downloaderPng(filePathName: str,ResponseContent:requests.models.Response):
    with open(filePathName, 'wb+') as pngFiles:
     for chunk in ResponseContent.iter_content(chunk_size=2048):
        pngFiles.write(chunk)
def downloader_bar(progressbar,startTime:float,end_time:float,process):
    for _ in progressbar:
        time.sleep(int(end_time - startTime) // 100)
        process += 1



def DownloaderFile(url: str, pathMethod: Literal['workPath', 'defaultPath', 'customerPath'] = 'defaultPath',
                   customerPath: str = '', defaultPathName: str = 'pjskPng', Referer_wedsite: str = None) -> None:
    if Referer_wedsite is None:
        Referer_wedsite = 'https://anime-pictures.net/'
    process = 0
    print(f"download from the the {url}")
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:145.0) Gecko/20100101 Firefox/145.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Cookie': f'sitelang=en;kira={random.randint(1,100)};priors={random.randint(1000,1000000)}',
               'Accept-Encoding': 'gzip,deflate,br,zstd',
               'Accept-Language': "zh-CN;q=0.9,en-US;q=0.8,en;q=0.7",
               'Referer': f"{Referer_wedsite}",
               'Connection': 'keep-alive',
               'Sec-Fetch-Dest': 'document',
               'Sec-Fetch-Mode': 'navigate',
               'Sec-Fetch-Site': 'same-site',
               'Sec_GPC':'1',
               }


    if  'https://oimages.anime-pictures.net' in url:
        FileName= url.split('-')[6].split('+')[0]+'.png'
    else:
       FileName = os.path.basename(url)
    try:

       with requests.get(url=url, headers=headers,timeout=30) as Png:
            content_type = Png.headers.get('Content-Type', '')
            print(content_type)
            if content_type in ['text/html']:
                raise urllib.error.URLError("download assert can not is html")
            else:
             with typer.progressbar(pictureBar(), length=100,color=True) as pro:

                match pathMethod:
                        case 'defaultPath':
                            startTime = perf_counter()
                            picturePath = os.path.join(os.getcwd(), defaultPathName, FileName)
                            downloaderPng(filePathName=picturePath, ResponseContent=Png)
                            endTime = perf_counter()
                            downloader_bar(progressbar=pro,startTime=startTime,end_time=endTime,process=process)
                        case 'customerPath':
                            startTime = perf_counter()
                            picturePath = os.path.join(os.getcwd(), customerPath, FileName)
                            downloaderPng(filePathName=picturePath, ResponseContent=Png)
                            endTime = perf_counter()
                            downloader_bar(progressbar=pro,startTime=startTime, end_time=endTime,process=process)
                        case 'workPath':
                            startTime = perf_counter()
                            downloaderPng(filePathName=os.path.join(os.getcwd(),FileName),ResponseContent=Png)
                            endTime = perf_counter()
                            downloader_bar(progressbar=pro,startTime=startTime, end_time=endTime,process=process)
    except TypeError:...








@CalculateAny
# its Decorators can calculate all thread download of time
def processPicture(urls: List[str], pathMethod: typing.Union[Literal['workPath', 'defaultPath', 'customerPath'], str] = 'defaultPath',
                   customerPath: str = '', defaultPathName: str = 'pjskPng',Referer_wedsite: str=None) -> None:
    """
    the Thread Event and Lock is not needs,so use the '#' to comment it
    """

    if urls:
        #pngLock = Lock()

        # PngThread = Thread(target=DownloaderFile, args=(urls[0], pngEvent))
        multiThreadDownload = (Thread(target=DownloaderFile, args=(urls[i], pathMethod, customerPath, defaultPathName,Referer_wedsite))
                               for i in
                               range(len(urls)))
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


@aqq.command()
def main(fatalist: Annotated[Optional[List[str]], typer.Argument(help='url from list')] = None,
         PathMethod: Annotated[str, typer.Option('--methods', '-M', help="this is the way to download the path way",
                                                 prompt='please enter your method')] = 'defaultPath',
         customerPath: Annotated[str, typer.Option('--customer', '-C', prompt="please input the path")] = '',
         defaultPathName: Annotated[
             str, typer.Option('--defaultPathName', '-D', prompt="please input the default path name")] = 'pjskPng',
             Referer_wedsite:Annotated[str,typer.Option('--Referer-wedsite','-R',prompt="please input the Referer_wedsite")] = None
         ):
    """
    workPath:download the picture in the work path\n
    defaultPath:download the picture in the default path\n
    customerPath:download the picture in the customer path\n


    :param Referer_wedsite: this is the  main wedsite on your download picture\n
    :param fatalist: the list of urls\n
    :param PathMethod: the method of download the path\n
    :param defaultPathName: is effect of the PathMethod in defaultPath,if the path is not exit of your computer,
    it has raise an error\n
    :param customerPath: if the path is not exit of your computer,is input has expected error
           else,you can download picture of your computer path
 """
    urlList = []
    methodList = ['workPath', 'defaultPath', 'customerPath']

    if PathMethod not in methodList:
        typer.Exit()
    else:
        for i in range(len(fatalist)):
            urlList.append(fatalist[i])
        processPicture(urls=urlList, pathMethod=PathMethod, customerPath=customerPath, defaultPathName=defaultPathName,Referer_wedsite=Referer_wedsite)
    #print(f"download picture is compete")


@aqq.command()
def watchMainDoc():
    print(main.__doc__)


if __name__ == "__main__":
    aqq()
