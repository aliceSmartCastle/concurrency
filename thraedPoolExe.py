import os.path
import time
from concurrent.futures.thread import ThreadPoolExecutor
from time import perf_counter
from urllib.request import urlopen
from FuncTip import spiteLine, GetterMemory,CalculateAny


def drive(ids):
    print(spiteLine(context=f'start driving {ids} thread'))
    time.sleep(1)
    return f"Done with task {ids}"

@CalculateAny
def pictureDownloader(url: str):
    PngData = None
    with urlopen(url) as wed:
        PngData = wed.read()
    if not PngData:
        raise Exception(f"Error: could not download the image from {url}")
    fileName = os.path.basename(url)
    ''''
    pngFile=open(os.path.join(fileName,'pjskPng','wb'))
    pngFile.write(PngData)
    print(f"{fileName} is download...")
    pngFile.close()
    '''
    with open(os.path.join(fileName,'pjskPng'), 'wb+') as pngFile:
        pngFile.write(PngData)
        print(f"{fileName} is download...")
        





def main():
    PngUrl = [ "https://wallpapercave.com/wp/wp9845704.jpg"
              'https://images3.alphacoders.com/128/thumb-1920-1289832.png',
              'https://images8.alphacoders.com/125/thumb-1920-1258396.jpg',
              'https://images7.alphacoders.com/129/thumb-1920-1292136.jpg',
              'https://images8.alphacoders.com/131/thumb-1920-1315968.png',
              'https://images6.alphacoders.com/120/thumb-1920-1208108.jpg',
              'https://images6.alphacoders.com/118/thumb-1920-1187050.png',
              'https://images8.alphacoders.com/128/thumb-1920-1284594.jpg',
              ]
    start = perf_counter()
    with ThreadPoolExecutor() as TheExe:
        TheExe.map(pictureDownloader,PngUrl)

       # f1=TheExe.submit(pictureDownloader,PngUrl[0])


    end = perf_counter()
    print(
        f"this took {end - start:4f} second(s) to finish")  #
    GetterMemory()


if __name__ == "__main__":
    main()
