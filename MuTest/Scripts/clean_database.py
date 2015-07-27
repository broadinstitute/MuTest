from MuTest.BasicUtilities.MongoUtilities import connect_to_mongo

def delete_all():
    variants = connect_to_mongo()
    variants.remove()

    normal_normal = connect_to_mongo(collection='NormalNormalData')
    normal_normal.remove()

if __name__ == '__main__':
    delete_all()