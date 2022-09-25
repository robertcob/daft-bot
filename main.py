from scraper.parseResults import pingPropertys
from daftdatabase.db import createInstance
from chatbots.discord import setupDiscord
import time
import pymongo

if __name__ == "__main__":
    db_intsance = createInstance()
    discordBot = setupDiscord()
    while True:
        newProperties = pingPropertys()
        for property in newProperties:
            try:
                db_intsance.insertProperty(property)
                discordBot.createMessage(property)
                if not property["owner_occupied"]:
                    discordBot.sendMessage()
                    db_intsance.numberOfDocuments()
                    time.sleep(2)
            except pymongo.errors.DuplicateKeyError:
                print("property already inserted!")
                continue
            except:
                break
        time.sleep(15)
        
            

