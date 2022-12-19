import cv2
import numpy as np
import math

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
    R = 2.0
    angle = 30.0
    h = R * math.cos(angle / 180 * math.pi)
    r = R * math.sin(angle / 180 * math.pi)
    x = r * averV * averS * math.cos(averH / 180.0 * math.pi)
    y = r * averV * averS * math.sin(averH / 180.0 * math.pi)
    z = h * (1 - averV)


    grar_aver = np.sum(gray) / 64
    gray_code = gray.copy()
    gray_code[gray_code < grar_aver] = 0
    gray_code[gray_code >= grar_aver] = 1
    gray_code = gray_code.flatten()
    gray_code = gray_code.astype(str)
    code = ''
    for string in gray_code:
        code = code + string
    code_int = int(code[:], 2)

    x = round(x,3)
    y = round(y,3)
    z = round(z,3)
    return (averH,averS,averV),code_int

#img = cv2.imread('DSC00550.JPG')
#print(analysis_HSV(img))