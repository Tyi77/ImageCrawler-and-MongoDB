import cv2
import numpy as np
import os
import Analysis_HSV
from tqdm import tqdm
import shutil
from multiprocessing.pool import Pool

def build(name):
    file = open('./database/attribute.txt', 'a')
    to_height = 100
    to_width = 100
    img = cv2.imread(f'./Image/{name}')
    # 裁切圖片為正方形
    if img.shape[0] > img.shape[1]:
        center = (int)(img.shape[0] / 2)
        length = (int)(img.shape[1] / 2)
        img = img[center - length:center + length, :, :]
    else:
        center = (int)(img.shape[1] / 2)
        length = (int)(img.shape[0] / 2)
        img = img[:, center - length:center + length, :]
    # 計算HSV和結構數據
    img = cv2.resize(img, (to_height, to_width), interpolation=cv2.INTER_AREA)
    HSV_aver, gray_code = Analysis_HSV.analysis_HSV(img)
    print(name, HSV_aver[0], HSV_aver[1], HSV_aver[2], gray_code, file=file)
    cv2.imwrite(f'./database/{name}', img)
    file.close()

if __name__ == '__main__':
    try:
        shutil.rmtree('./database')
    except:
        pass
    os.mkdir('./database')
    data_name = os.listdir('./Image')
    with Pool() as pool:
        list(tqdm(pool.imap(build,data_name), colour='WHITE', desc="build database", total=len(data_name)))
    pool.close()
    pool.join()
