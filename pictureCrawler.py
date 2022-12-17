import requests
import os
import concurrent.futures
from itertools import compress

def crawler(args):
    '''args 0: idx, 1: url'''
    img = requests.get(args[1])
    try:
        img.content.decode('utf-8')
        return False # Nonvalid
    except:
        pass

    with open(f'./images/{args[0]}.jpg', 'wb') as file:
        file.write(img.content)
    print(args[0], args[1])
    return True # Valid

def crawl_images(startIdx: int, endIdx: int) -> list:
    '''Download images.\n\nThe range of index is [startIdx, endIdx)\n\nValid index: [1, 1000000]\n\nReturn (index, url) list of downloaded images.'''
    # flag = True
    # while flag:
    #     inputRange = input('What range do you want[MIN:MAX){1-1000000}: ')
    #     try:
    #         inputRange = [int(item.strip()) for item in inputRange.split(':')]
    #         if len(inputRange) != 2:
    #             print('You enter wrong pattern.')
    #         else:
    #             flag = False
    #     except:
    #         print('You enter wrong pattern.')

    # ---Check the folder which places images exists---
    if not os.path.exists('./images'):
        os.mkdir('./images')
    
    # ---Build the url list---
    imageURLs = [] # (idx, url)
    with open('./open-images-dataset-train0.tsv', 'r') as file:
        inputIdx = range(startIdx, endIdx)
        for idx, line in enumerate(file):
            if idx in inputIdx:
                url = line.split('\t')[0]
                imageURLs.append([idx, url])
    with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
        filter_ = executor.map(crawler, imageURLs)
    
    idxList, urlList = [], []
    for e in compress(imageURLs, filter_):
        idxList.append(e[0])
        urlList.append(e[1])
    
    return idxList, urlList