from pymongo import MongoClient
import pymongo
from itertools import filterfalse

def get_db(hostIP: str, port: int) -> tuple:
    '''Return database and collection'''
    client = MongoClient(hostIP, port) # Connection

    db = client['ImagesDB']
    global coll
    coll = db['ImagesColl']

    # ---Check if the user wants to drop the db---
    if input('Do you want to clear the ImagesDB? (y/n): ') == 'y':
        if input ('Are you sure to delete all the data in ImagesDB? (y/n): ') == 'y':
            client.drop_database(client['ImagesDB'])
            print('System: Cleared the ImagesDB.')

    return db, coll

def insert_image(coll, doc: dict):
    ''' Insert one document'''
    idx = doc['_id']
    if list(coll.find_one({'_id': idx})) == []:
        coll.insert_one(doc)

def insert_images(coll, docList: list):
    '''Insert multiple documents.'''
    startIdx = docList[0]['_id']
    endIdx = docList[-1]['_id']

    existingDocs = coll.find({'_id': {'$gte': startIdx, '$lt': endIdx}})
    needInsertedDocList = list(filterfalse(lambda x: x in existingDocs, docList)) # Output False elements(not output True elements)
    
    if needInsertedDocList != []:
        coll.insert_many(needInsertedDocList)

def delete_images_by_regex(coll, field: str, regex: str):
    coll.delete_many({
        field: {'$regex': regex}
    })

def find_15th_great_images(coll, h, s, v):
    return coll.aggregate([{
        '$project': {
            '_id': 1,
            'dist': {
                '$add': [
                    {'$pow': [ { '$subtract': [ {'$arrayElemAt': [ "$hsv_aver", 0 ]}, h]}, 2 ]},
                    {'$pow': [ { '$subtract': [ {'$arrayElemAt': [ "$hsv_aver", 1 ]}, s] }, 2 ]},
                    {'$pow': [ { '$subtract': [ {'$arrayElemAt': [ "$hsv_aver", 2 ]}, v] }, 2 ]}
                ]
            },
            'gray_code': 1
        }},
        {'$sort':{'dist': pymongo.ASCENDING}},
        {'$limit': 15}
    ])
    
    # return coll.find({'_id': 1}).limit(15)