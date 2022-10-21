from scraper.daftLibrary import executeDaft
from chatbots.discordMessageSend import setupDiscord
import time
import os
import pickle as pkl
from chatbots.discordBot import run
import threading
import time

PATH = os.path.dirname(os.path.abspath(__file__))

def get_cache(filepath=os.path.join(PATH, 'cache.pkl')):
    if os.path.exists(filepath):
        with open(filepath, mode='rb') as fd:
            cache = pkl.load(fd)
    else:
        cache = set()
    return cache

if __name__ == "__main__":
    discordBot = setupDiscord()
    discordThread = threading.Thread(target=run, args=(os.environ['DISCORDSECRET'],))
    discordThread.start()
    daft = executeDaft()
    cache = get_cache()
    while True:
        listings = daft.setListings()
        newProperties = [x for x in daft.exportListings(listings) if x['_id'] not in cache]
        for property in newProperties:
            try:
                discordBot.createMessage(property)
                discordBot.sendMessage()
                time.sleep(3)
                cache.add(property['_id'])
            except Exception as e:
                print(e)
                raise
        time.sleep(15)
        
            

