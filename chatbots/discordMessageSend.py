import requests
import json
class Discord:
    def __init__(self, token) -> None:
        self.token = token
        self.message = None
        self.channel = "https://discord.com/api/v9/channels/1023308481970835567/messages"
    
    def setMessage(self, newMessage) -> None:
        self.message = newMessage
    
    def cleanDescription(self, rawDesc):
        n = 121
        outputStr = ""
        clean = [rawDesc[i:i + n] for i in range(0, len(rawDesc), n)]
        for line in clean:
            outputStr += "\t\t"
            outputStr += line
            outputStr += "\n"
        return outputStr

    def createMessage(self, propertyObj):
        barrier = "##########################"
        cleanDesc = propertyObj['extra']['description']
        
        message = '''NEW PROPERTY! 🏠  \n- Property price 💸: %d\n- Room for rent in %s\n- Link To Property %s\n- Property Publish Date ⏰: %s\n- Type of bedroom 🚽: %s\n\n- Description of property:\n %s\n%s\n%s\n'''%(int(propertyObj['price']), propertyObj['address'], propertyObj['url'],
         propertyObj['extra']['publish_date'], propertyObj['extra']['bedrooms'], cleanDesc, barrier, barrier)
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
    discord = Discord(token)
    return discord