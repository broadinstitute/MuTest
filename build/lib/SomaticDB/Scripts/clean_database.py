from SomaticDB.BasicUtilities.MongoUtilities import connect_to_mongo

def delete_all():
    variants = connect_to_mongo()
    variants.remove()

if __name__ == '__main__':
    delete_all()