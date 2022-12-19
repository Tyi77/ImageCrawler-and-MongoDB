from pictureCrawler import crawl_images
from createDocument import create_document_list
import dbController

def example_start():
    idxList, urlList = crawl_images(20, 30)
    db, coll = dbController.create_db('localhost', 27017)
    c_a = range(10)
    s_a = range(10, 0, -1)
    needInsertedList = create_document_list(idxList, urlList, c_a, s_a)
    dbController.insert_images(coll, needInsertedList)

if __name__ == '__main__':
    example_start()