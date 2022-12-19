import cv2
import numpy as np
from multiprocessing import Pool
from tqdm import tqdm

from pictureCrawler import crawl_images
from db.createDocument import create_document
import db.dbController as dbController

def insert_analyzed_images(idx):
    img = cv2.imread(f'./Image/{idx}.jpg')
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(cv2.resize(img, (8,8), interpolation=cv2.INTER_AREA),cv2.COLOR_BGR2GRAY)

    H, S, V = cv2.split(hsv)
    aH = np.array(H).flatten()
    aS = np.array(S).flatten()
    aV = np.array(V).flatten()
    averH = np.sum(aH)/aH.shape[0]
    averS = np.sum(aS)/aS.shape[0]
    averV = np.sum(aV)/aV.shape[0]


    grar_aver = np.sum(gray) / 64
    gray_code = gray.copy()
    gray_code[gray_code < grar_aver] = 0
    gray_code[gray_code >= grar_aver] = 1
    gray_code = gray_code.flatten()
    gray_code = gray_code.astype(str)
    code = ''
    for string in gray_code:
        code = code + string
    # code_int = int(code[:], 2)

    return create_document(idx, f'{idx}.jpg', (averH,averS,averV), code)

def analysis_HSV(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(cv2.resize(img, (8,8), interpolation=cv2.INTER_AREA),cv2.COLOR_BGR2GRAY)

    H, S, V = cv2.split(hsv)
    aH = np.array(H).flatten()
    aS = np.array(S).flatten()
    aV = np.array(V).flatten()
    averH = np.sum(aH)/aH.shape[0]
    averS = np.sum(aS)/aS.shape[0]
    averV = np.sum(aV)/aV.shape[0]

    grar_aver = np.sum(gray) / 64
    gray_code = gray.copy()
    gray_code[gray_code < grar_aver] = 0
    gray_code[gray_code >= grar_aver] = 1
    gray_code = gray_code.flatten()
    gray_code = gray_code.astype(str)
    code = ''
    for string in gray_code:
        code = code + string

    return (averH,averS,averV), code

def HSV_dis(HSV1,HSV2):
    dis = 0
    for i in range(3):
        dis += (HSV1[i] - HSV2[i])**2
    return dis**0.5

def hamming_dis(code1,code2):
    return bin(int(code1, 2) ^ int(code2, 2)).count('1')


def build_ImagesDB(startIdx: int, endIdx: int):
    idxList = crawl_images(startIdx, endIdx)

    with Pool(processes=20) as pool:
        result = list(tqdm(pool.imap(insert_analyzed_images, idxList), colour='WHITE', desc="build database", total=len(idxList)))

    db, coll = dbController.get_db('localhost', 27017)
    dbController.insert_images(coll, list(result))

def start(targetName: str):
    db, coll = dbController.get_db('localhost', 27017)

    tile, to_height, to_width = 10000, 100, 100

    target = cv2.imread(targetName)
    if target.shape[0] > target.shape[1]:
        multiple = target.shape[0] / target.shape[1]
        edge_tile = (int)((tile / multiple)**0.5) + 1
        new_height = (int)(edge_tile * multiple) * to_height
        new_width = edge_tile * to_width
        height_tile = (int)(edge_tile * multiple)
        width_tile = edge_tile
    else:
        multiple = target.shape[1] / target.shape[0]
        edge_tile = (int)((tile / multiple) ** 0.5) + 1
        new_height = edge_tile * to_height
        new_width = (int)(edge_tile * to_width * multiple)
        height_tile = edge_tile
        width_tile = (int)(edge_tile * multiple)

    target = cv2.resize(target,(new_width,new_height),interpolation=cv2.INTER_CUBIC)
    total = height_tile * width_tile
    mapping_table = [[None for col in range(width_tile)] for row in range(height_tile)]
    with tqdm(total=total, desc='Caculte mapping table', colour='WHITE', unit='tiles') as pbar:
        for i in range(height_tile):
            for j in range(width_tile):
                tmp = target[i*to_height:(i+1)*to_height,j*to_width:(j+1)*to_width,:]
                mapping_table[i][j] = analysis_HSV(tmp)
                pbar.update(1)

    # file = open('database/attribute.txt','r')
    # data = file.readlines()
    # file.close()
    # database = [None for i in range(len(data))]
    # count = 0
    # for line in data:
    #     tmp = line.split(' ')
    #     try:
    #         database[count] = (tmp[0], ((float)(tmp[1]), (float)(tmp[2]), (float)(tmp[3])), (int)(tmp[4]))
    #         count += 1
    #     except:
    #         print(f'line {count} occar an error')
    #         del database[-1]
    # database = np.array(database,dtype=object)

    product = target.copy()
    with tqdm(total=total, desc='creating image', colour='WHITE', unit='tiles') as pbar:
        for i in range(height_tile):
            for j in range(width_tile):
                pbar.update(1)
                HSV_coordinate = mapping_table[i][j][0]
                gray_code = mapping_table[i][j][1]
                # HSV_dist = [9999 for i in range(len(database))]
                # count = 0
                # for data in database:
                #     HSV_dist[count] = HSV_dis(HSV_coordinate,data[1])
                #     count+=1
                HSV_dist = dbController.find_15th_great_images(coll, HSV_coordinate[0], HSV_coordinate[1], HSV_coordinate[2])
                winner = [9999,0] #hamming dis,index
                for doc in HSV_dist:
                    # closest = min(HSV_dist)
                    # index = HSV_dist.index(closest)
                    # HSV_dist[index] = 9999
                    dis = hamming_dis(gray_code, doc['gray_code'])
                    if dis < winner[0]:
                        winner[0] = dis
                        winner[1] = doc['_id']
                tmp_img = cv2.imread(f'./Image/{winner[1]}.jpg')
                product[i*to_height:(i+1)*to_height,j*to_width:(j+1)*to_width,:] = tmp_img
    cv2.imwrite('HSV_first.jpg',product)
    overlapping = cv2.addWeighted(product, 0.8, target, 0.2, 0)
    cv2.imwrite('HSV_product.jpg', overlapping)

if __name__ == '__main__':
    # build_ImagesDB(1001, 2000)
    start('ABC.jpg')