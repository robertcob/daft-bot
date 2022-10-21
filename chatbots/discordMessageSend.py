import requests
import json
import os
class Discord:
    def __init__(self, token, channel) -> None:
        self.token = token
        self.message = None
        self.channel = channel
    
    def setMessage(self, newMessage) -> None:
        self.message = newMessage

    def createMessage(self, propertyObj):
        barrier = "##########################"
        
        message = '''NEW PROPERTY! 🏠  \n- Property price 💸: %d\n- Room for rent in %s\n- Link To Property %s\n- Property Publish Date ⏰: %s\n- Type of bedroom 🚽: %s\n\n- Description of property:\n %s\n%s\n'''%(int(propertyObj['price']), propertyObj['address'], propertyObj['url'],
         propertyObj['extra']['publish_date'], propertyObj['extra']['bedrooms'], barrier, barrier)
        self.setMessage(message)
    
    def sendMessage(self):
        POSTedJSON  = json.dumps({
            'content': self.message
        })
        headers = { "Authorization":"Bot {}".format(self.token),
                    "User-Agent":"myBotThing (http://some.url, v0.1)",
                    "Content-Type":"application/json", }

        resp = requests.post(self.channel, data=POSTedJSON, headers=headers)
        print(resp.status_code)

def setupDiscord():
    token = input("Please input discord api key: ")
    channel = input("Please input channel url: \n")
    os.environ['DISCORDSECRET'] = token
    discord = Discord(token, channel)
    return discord