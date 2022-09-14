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
        print("entered property with id %s into properties db".format(id))
    
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

# Driver code

usernameENV = input("Input Username ")
userENVSecret = input("Input Secret ")
connectionString  = f"mongodb+srv://{usernameENV}:{userENVSecret}@cluster0.g6xzti4.mongodb.net/test"
client = MongoClient(connectionString)

# testData1 = {'_id': '4087460', 'url': 'https://www.daft.ie/share/inchicore-inchicore-dublin-8/4087460', 'price': 1000, 'address': 'inchicore inchicore dublin 8', 'owner_occupied': False, 'preferences': 'Male', 'sharing_number': 4, 'duration': '1Year', 'extra': {'start': 'Immediately', 'description': 'Double room in Inchicore Dublin 8, looking for single male only,  non party and smoking and easy going person. Rent 1000 plus bills, deposit one month , few min to the luas station and bus stop, walking distance to Tesco Aldi, around 30min to tcd ,and 25 to grinfith college. Easy to get in to the city Centre, contact me for more imformation and  viewing thanks', 'payment_interval': 'Month', 'bathroom_type': 'Shared Bathroom', 'bedrooms': 1, 'property_type': 'House'}}
# testData2 = {'_id': '999999', 'url': 'https://www.daft.ie/share/inchicore-inchicore-dublin-8/999999', 'price': 1000, 'address': 'inchicore inchicore dublin 8', 'owner_occupied': False, 'preferences': 'Male', 'sharing_number': 4, 'duration': '1Year', 'extra': {'start': 'Immediately', 'description': 'Double room in Inchicore Dublin 8, looking for single male only,  non party and smoking and easy going person. Rent 1000 plus bills, deposit one month , few min to the luas station and bus stop, walking distance to Tesco Aldi, around 30min to tcd ,and 25 to grinfith college. Easy to get in to the city Centre, contact me for more imformation and  viewing thanks', 'payment_interval': 'Month', 'bathroom_type': 'Shared Bathroom', 'bedrooms': 1, 'property_type': 'House'}}

# testDatabase = Database(client, 'daft', 'daft-shared-rooms')
# testDatabase.insertProperty(testData1)
# testDatabase.insertProperty(testData2)
# testDatabase.numberOfDocuments()
# testDatabase.findProperty("4087460")
# testDatabase.removeProperty("999999")
# testDatabase.numberOfDocuments()



