from pymongo import MongoClient

client = MongoClient("mongodb://root:password@mongo:27017")
# DB接続(存在しない場合は作成)
db = client["testdb"]
# collection接続(存在しない場合は作成)
collection = db["test_collection"]

# 1件登録
collection.insert_one({"name": "TestA", "age": 100})

client.close()
