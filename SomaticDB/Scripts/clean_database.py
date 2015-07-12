from SomaticDB.BasicUtilities.MongoUtilities import connect_to_mongo

variants = connect_to_mongo()
variants.remove()
