from pymongo import MongoClient

class Database:
    def __init__(self, client, db_name, collection_name) -> None:
        self.client = client
        self.db = self.setDatabase(db_name)
        self.col = self.setCollection(collection_name)

    def setDatabase(self, db_name):
        try:
            return self.client[db_name]
        except:
            print("failed to get database " + db_name) 
    
    def setCollection(self, collection_name):
        try:
            return self.db[collection_name]
        except:
            print("failed to get collection " + collection_name)
    
    def insertProperty(self, property):
        id = self.col.insert_one(property)
    
    def findProperty(self, id):
        result = self.col.find_one({"_id": id})
        print("found Property!")
        print(result)
    
    def removeProperty(self, id):
        result = self.col.delete_one({"_id": id})
        print("deleted property")
        print(result)
    
    def numberOfDocuments(self):
        return self.col.count_documents({})

def createInstance():
    usernameENV = input("Input Username ")
    userENVSecret = input("Input Secret ")
    connectionString  = f"mongodb+srv://{usernameENV}:{userENVSecret}@cluster0.g6xzti4.mongodb.net/test"
    client = MongoClient(connectionString)
    return Database(client, 'daft', 'daft-shared-rooms')



