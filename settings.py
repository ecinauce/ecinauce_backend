import pymongo

con = pymongo.MongoClient("localhost", 27017)
project_db = con["resume_testdb"]
project_accounts_db = con["resume_testdb_accounts"]