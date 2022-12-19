import numpy as np
import cv2
import Analysis_HSV
from tqdm import tqdm

tile = 5000
to_height = 100
to_width = 100

def HSV_dis(HSV1,HSV2):
    dis = 0
    for i in range(3):
        dis += (HSV1[i] - HSV2[i])**2
    return dis**0.5

def hamming_dis(code1,code2):
    return bin((int)(code1) ^ (int)(code2)).count("1")

target = cv2.imread('DSC00691.JPG')
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
            mapping_table[i][j] = Analysis_HSV.analysis_HSV(tmp)
            pbar.update(1)

file = open('database/attribute.txt','r')
data = file.readlines()
file.close()
database = [None for i in range(len(data))]
count = 0
for line in data:
    tmp = line.split(' ')
    try:
        database[count] = (tmp[0], ((float)(tmp[1]), (float)(tmp[2]), (float)(tmp[3])), (int)(tmp[4]))
        count += 1
    except:
        print(f'line {count} occar an error')
        del database[-1]
database = np.array(database,dtype=object)

product = target.copy()
with tqdm(total=total, desc='creating image', colour='WHITE', unit='tiles') as pbar:
    for i in range(height_tile):
        for j in range(width_tile):
            pbar.update(1)
            HSV_coordinate = mapping_table[i][j][0]
            gray_code = mapping_table[i][j][1]
            HSV_dist = [9999 for i in range(len(database))]
            count = 0
            for data in database:
                HSV_dist[count] = HSV_dis(HSV_coordinate,data[1])
                count+=1
            winner = [9999,0] #hamming dis,index
            for c in range(15):
                closest = min(HSV_dist)
                index = HSV_dist.index(closest)
                HSV_dist[index] = 9999
                dis = hamming_dis(gray_code, database[index,2])
                if dis < winner[0]:
                    winner[0] = dis
                    winner[1] = index
            tmp_img = cv2.imread(f'./database/{database[winner[1],0]}')
            product[i*to_height:(i+1)*to_height,j*to_width:(j+1)*to_width,:] = tmp_img
cv2.imwrite('HSV_first.jpg',product)
overlapping = cv2.addWeighted(product, 0.8, target, 0.2, 0)
cv2.imwrite('HSV_product.jpg', overlapping)
