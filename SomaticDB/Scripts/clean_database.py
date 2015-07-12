from SomaticDB.BasicUtilities.MongoUtilities import connect_to_mongo

def main():
    variants = connect_to_mongo()
    variants.remove()

if __name__ == '__main__':
    main()
