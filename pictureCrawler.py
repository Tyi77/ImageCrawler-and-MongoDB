from io import BytesIO
import requests
import os
import cv2
import numpy as np
import concurrent.futures
from itertools import compress
import imageio

def build(img, name):
    to_height = 100
    to_width = 100
    # 裁切圖片為正方形
    if img.shape[0] > img.shape[1]:
        center = (int)(img.shape[0] / 2)
        length = (int)(img.shape[1] / 2)
        try:
            img = img[center - length:center + length, :, :]
        except:
            cv2.imwrite(name, img)
    else:
        center = (int)(img.shape[1] / 2)
        length = (int)(img.shape[0] / 2)
        try:
            img = img[:, center - length:center + length, :]
        except:
            cv2.imwrite(name, img)
    # 計算HSV和結構數據
    img = cv2.resize(img, (to_height, to_width), interpolation=cv2.INTER_AREA)
    cv2.imwrite(f'./Image/{name}', img)

def crawler(args):
    '''Used by the func crawl_images\n\nargs: 0/idx, 1/url'''
    res = requests.get(args[1])
    try:
        res.content.decode('utf-8')
        return False # Nonvalid
    except:
        pass
    img_arr = imageio.imread(BytesIO(res.content))
    img_arr = cv2.cvtColor(img_arr, cv2.COLOR_RGB2BGR)
    build(img_arr, f'{args[0]}.jpg')
    # with open(f'./Image/{args[0]}.jpg', 'wb') as file:
    #     file.write(img.content)

    # print(args[0], args[1])
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
    if not os.path.exists('./Image'):
        os.mkdir('./Image')
    
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
    
    idxList = []
    for e in compress(imageURLs, filter_):
        idxList.append(e[0])
    
    return idxList