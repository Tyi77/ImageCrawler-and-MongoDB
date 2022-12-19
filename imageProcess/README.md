Analysis_HSV：
分析圖片屬性，會回傳HSV分別的平均(Haver,Saver,Vacer)和轉換成int的8*8結構代碼(code_int)  

build_database：
從資料庫中讀取圖片，裁切成正方形後分析屬性，會創建/database資料夾，裡面會有縮小後的圖片和紀錄屬性的文檔attribute.txt 
(有用pool來加速分析，CPU吃滿是正常情況)  

create_img：
target是要合成的圖片，可以調整開頭的tile來決定要用多少圖來組合，目前為了材料圖片的清晰程度，統一是用100\*100，所以用的照片越多圖片檔案會越大
