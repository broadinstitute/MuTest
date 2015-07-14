from pymongo import MongoClient

def connect_to_mongo():
    client = MongoClient('104.197.21.136',27017)
    client.somatic_db_master.authenticate('kareem', 'p1IU5lec5WM7NeA')
    db = client['somatic_db_master']
    variants = db['ValidationData']
    return variants

