import requests

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
        cleanDesc = self.cleanDescription(propertyObj['extra']['description'])
        
        message = '''NEW PROPERTY! 🏠  \n- Property price 💸: %d\n- Room for rent in %s\n- Sharing with %d people 🧑‍🤝‍🧑\n- Duration of rental ⏰: %s\n- Preferences: %s\n- Type of bathroom 🚽: %s\n\n- Description of property:\n %s%s\n%s\n'''%(int(propertyObj['price']), propertyObj['address'], int(propertyObj['sharing_number']),
         propertyObj['duration'], propertyObj['preferences'], propertyObj['extra']['bathroom_type'], cleanDesc, barrier, barrier)
        self.setMessage(message)
    
    def sendMessage(self):
        payload = {
            'content': self.message
        }
        header = {
            'authorization' : self.token 
        }
        requests.post(self.channel, data=payload, headers=header)

def setupDiscord():
    token = input("Please input discord api key: ")
    discord = Discord(token)
    return discord

# channelURL = "https://discord.com/api/v9/channels/1023308481970835567/messages"
# testData1 = {'_id': '4087460', 'url': 'https://www.daft.ie/share/inchicore-inchicore-dublin-8/4087460', 'price': 1000, 'address': 'inchicore inchicore dublin 8', 'owner_occupied': False, 'preferences': 'Male', 'sharing_number': 4, 'duration': '1Year', 'extra': {'start': 'Immediately', 'description': 'Double room in Inchicore Dublin 8, looking for single male only,  non party and smoking and easy going person. Rent 1000 plus bills, deposit one month , few min to the luas station and bus stop, walking distance to Tesco Aldi, around 30min to tcd ,and 25 to grinfith college. Easy to get in to the city Centre, contact me for more imformation and  viewing thanks', 'payment_interval': 'Month', 'bathroom_type': 'Shared Bathroom', 'bedrooms': 1, 'property_type': 'House'}}
# discord = Discord(token, channelURL)
# discord.createMessage(testData1)
# discord.sendMessage()