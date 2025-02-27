#!/usr/bin/python3

##############################################################################################################
#                                CLASSES CONTAINING ALL THE APP FUNCTIONS                                    #
##############################################################################################################

class DB:

    def __init__(self, Config):
        from math import floor
        from os import getcwd
        from os.path import join
        from json import loads, dumps, dump
        from datetime import timedelta, datetime, timezone 
        from pymongo import MongoClient, errors, ReturnDocument
        from urllib import parse
        from urllib.request import urlopen 
        from bson.objectid import ObjectId  
       
        self.Config          = Config
        self.getcwd          = getcwd
        self.join            = join 
        self.floor           = floor 
        self.loads           = loads
        self.dumps           = dumps
        self.dump            = dump  
        self.datetime        = datetime
        self.ObjectId        = ObjectId 
        self.server          = Config.DB_SERVER
        self.port            = Config.DB_PORT
        self.username        = parse.quote_plus(Config.DB_USERNAME)
        self.password        = parse.quote_plus(Config.DB_PASSWORD)
        self.remoteMongo     = MongoClient
        self.ReturnDocument  = ReturnDocument
        self.PyMongoError    = errors.PyMongoError
        self.BulkWriteError  = errors.BulkWriteError  
        self.tls             = False  # MUST SET TO TRUE IN PRODUCTION

    def __del__(self):
        # Delete class instance to free resources
        pass


    ####################
    # LAB 4 FUNCTIONS  #
    ####################

   # 1. FUNCTION TO INSERT DATA INTO THE RADAR COLLECTION
    def insert_data(self, data):
        '''Insert data into the radar collection'''
        try:
            remotedb = self.remote_mongo(
                f'mongodb://{self.username}:{self.password}@{self.server}:{self.port}', 
                tls=self.tls
            )
            result = remotedb.ELET2415.radar.insert_one(data)
        except Exception as e:
            print(f"insert_data error: {e}")    
            return None
        return result

    # 2. FUNCTION TO RETRIEVE DOCUMENTS FROM RADAR COLLECTION BETWEEN DATE RANGE
    def retrieve_radar(self, start, end):
        '''Retrieves documents from the 'radar' collection within the specified date range'''
        try:
            start, end = int(start), int(end)

            remotedb = self.remote_mongo(
                f'mongodb://{self.username}:{self.password}@{self.server}:{self.port}', 
                tls=self.tls
            )
            result = remotedb.ELET2415.radar.find(
                {"timestamp": {"$gte": start, "$lte": end}, "reserve": {"$exists": True}},
                {"_id": 0, "timestamp": 1, "reserve": 1, "waterheight": 1}
            )
        except Exception as e:
            print(f"retrieve_radar error: {e}")
            return None
        return result

    # 3. FUNCTION TO COMPUTE AVERAGE 'reserve' VALUE
    def average_radar(self, start, end):
        '''Computes the arithmetic average on the 'reserve' field'''
        try:
            start, end = int(start), int(end)

            remotedb = self.remote_mongo(
                f'mongodb://{self.username}:{self.password}@{self.server}:{self.port}', 
                tls=self.tls
            )
            result = remotedb.ELET2415.radar.aggregate([
                {"$match": {"timestamp": {"$gte": start, "$lte": end}}},
                {"$group": {"_id": None, "average": {"$avg": "$reserve"}}},
                {"$project": {"_id": 0, "average": 1}}
            ])
        except Exception as e:
            print(f"average_radar error: {e}")
            return None
        return result

    # 4. FUNCTION TO INSERT/UPDATE PASSCODE IN THE 'code' COLLECTION
    def set_pass(self, passcode):
        '''Update the document in the 'code' collection with the new passcode'''
        passcode = str(passcode)
        try:
            remotedb = self.remote_mongo(
                f'mongodb://{self.username}:{self.password}@{self.server}:{self.port}', 
                tls=self.tls
            )

            collection = remotedb.ELET2415.code  # Ensure collection access is correct

            item = collection.find_one_and_update(
                {"type": "passcode"},
                {"$set": {"code": passcode}},
                upsert=True,
                projection={"_id": False},
                return_document=self.ReturnDocument.AFTER
            )

        except Exception as e:
            print(f"set_pass error: {e}")
            return None
        return item  

    # 5. FUNCTION TO COUNT PASSCODES IN 'code' COLLECTION
    def count_passcodes(self, passcode):
        '''Returns the number of times a passcode appears in the 'code' collection'''
        try:
            passcode = str(passcode)

            remotedb = self.remote_mongo(
                f'mongodb://{self.username}:{self.password}@{self.server}:{self.port}', 
                tls=self.tls
            )
            result = remotedb.ELET2415.code.count_documents({"code": passcode})
        except Exception as e:
            print(f"count_passcodes error: {e}")
            return None
        return result


def main():
    from config import Config
    from time import time

    db = DB(Config)

    start = time()
    # You can add test cases here to call class methods
    end = time()

    print(f"Completed in: {end - start} seconds")
    
if __name__ == '__main__':
    main()
