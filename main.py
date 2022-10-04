from daftdatabase.db import createInstance
from scraper.daftLibrary import executeDaft
from chatbots.discordMessageSend import setupDiscord
import time
import pymongo

if __name__ == "__main__":
    db_intsance = createInstance()
    discordBot = setupDiscord()
    daft = executeDaft()
    while True:
        listings = daft.setListings()
        newProperties = daft.exportListings(listings)
        for property in newProperties:
            try:
                db_intsance.insertProperty(property)
                discordBot.createMessage(property)
                discordBot.sendMessage()
                db_intsance.numberOfDocuments()
                time.sleep(2)
            except pymongo.errors.DuplicateKeyError:
                print("property already inserted!")
                continue
            except Exception as e:
                print(e)
                raise
        time.sleep(15)
        
            

