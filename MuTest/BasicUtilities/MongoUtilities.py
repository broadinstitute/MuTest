from pymongo import MongoClient


# def connect_to_mongo(collection='ValidationData'):
#     client = MongoClient('104.197.21.136',27017)
#     client.somatic_db_master.authenticate('kareem', 'p1IU5lec5WM7NeA')
#     db = client['somatic_db_master']
#     variants = db[collection]
#     return variants

def connect_to_mongo(collection='ValidationData'):
    client = MongoClient('69.173.65.108',27017)
    client.somatic_db_master.authenticate('kareem', 'p1IU5lec5WM7NeA')
    db = client['somatic_db_master']
    variants = db[collection]
    return variants



#mongo 104.197.21.136 -u kareem -p p1IU5lec5WM7NeA
#use somatic_db_master

#mongo 69.173.65.108 -u kareem -p p1IU5lec5WM7NeA