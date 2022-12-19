import os

from db.pictureCrawler import crawl_images
from db.createDocument import create_document_list
import db.dbController as dbController

def example_start():
    idxList, urlList = crawl_images(20, 30)
    data_name = os.listdir('./Image')
    db, coll = dbController.create_db('localhost', 27017)
    c_a = range(10)
    s_a = range(10, 0, -1)
    needInsertedList = create_document_list(idxList, urlList, c_a, s_a)
    dbController.insert_images(coll, needInsertedList)

if __name__ == '__main__':
    example_start()