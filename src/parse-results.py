from tkinter import N
import requests
from bs4 import BeautifulSoup
import re

class Property:
    def __init__(self) -> None:
        self.id = None
        self.url = None
        self.price = None
        self.address = None
        self.occupied = None
        self.roomType = None
        self.preferences = None
        self.sharing = None
        self.duration = None
        self.startDate = None
        self.description = None
        self.interval = None
        self.bathroom = None
        self.propertyType = None
        self.bedrooms = None
    
    def setID(self, newID):
        self.id = newID
    
    def setURL(self, newURL):
        self.url = newURL
    
    def setPrice(self, newPrice):
        self.price = newPrice
    
    def setAddress(self, newAddress):
        self.address = newAddress
    
    def setOccupied(self, newOccupied):
        self.occupied = newOccupied
    
    def setRoomType(self, newRoomType):
        self.roomType = newRoomType
    
    def setPreferences(self, newPreferences):
        self.preferences = newPreferences
    
    def setSharing(self, newSharing):
        self.sharing = newSharing
    
    def setDuration(self, newDuration):
        self.duration = newDuration
    
    def setStartDate(self, newStartDate):
        self.startDate = newStartDate
    
    def setDescription(self, newDescription):
        self.description = newDescription
    
    def setInterval(self, newPaymentInterval):
        self.interval = newPaymentInterval
    
    def setBathroom(self, newBathroomType):
        self.bathroom = newBathroomType
    
    def setPropertyType(self, newPropertyType):
        self.propertyType = newPropertyType
    
    def setNumBedrooms(self, newNumBedrooms):
        self.bedrooms = newNumBedrooms

    def exportData(self):
        data =  {
            'id': self.id, ##get from parsing the URL
            'url': self.url,
            'price': self.price,
            'address': self.address,
            'owner_occupied': self.occupied,
            'preferences' : self.preferences,
            'sharing_number': self.sharing,
            'duration': self.duration,    
            'extra': {
                "start" : self.startDate,
                'description': self.description,
                'payment_interval': self.interval,
                'bathroom_type': self.bathroom,
                "bedrooms": self.bedrooms,
                'property_type': self.propertyType
                }
            }
        return data

class PropertyParser:
    def __init__(self, location, priceFrom, priceTo) -> None:
        self.priceFrom = str(priceFrom)
        self.priceTo = str(priceTo)
        self.location = str(location)
        self.newProperties = []

    ### returns url of all current rental rooms in duration
    def pingDaft(self):
        pingURL = "https://www.daft.ie/sharing/{}?rentalPrice_from={}&rentalPrice_to={}&sort=publishDateDesc".format(self.location, self.priceFrom, self.priceTo)
        resp = requests.get(pingURL)
        propertysURLRegex = re.compile("^/share")
        if resp.status_code == 200:
            html_doc = resp.content
            soup = BeautifulSoup(html_doc, 'html.parser')
            content = soup.find_all("a", href=True)
            diff = [link['href'] for link in content if re.match(propertysURLRegex, link['href'])]
            #TODO database crap...
            if len(diff) > 0:
                self.exportProperties(diff)
        else:
            print("bad daft url!")

    def parseURLAddress(self, url):
        data = url.split("/")
        addData = data[2].split('-')
        address = " ".join(addData)
        return address

    def parseUrlID(self, url):
        data = url.split("/")
        addData = data[3].split('-')
        id = " ".join(addData)
        return id
    
    def parsePrice(self, raw):
        price = int(re.sub('[^0-9]','', raw))
        if price > 300:
            return [price, "Month"]
        else:
            return [price, "Week"]
        
    def setOwnerOccupied(self, data):
        if data == "No" or data == "no":
            return False
        else:
            return True
    
    def cleanDescription(self, rawDescription):
        rawDescription = rawDescription.replace("Description", "")
        clean = re.sub("/[^A-Za-z0-9 ]/", "", rawDescription)
        return clean.replace("\n", "")


    def exportProperties(self, newPropetyURLs):
        priceRegex = re.compile("^TitleBlock__Price")
        roomInfoRegex = re.compile("^TitleBlock__CardInfo")
        overViewRegex = re.compile("^styles__InfoSection")
        for url in newPropetyURLs:
            currProperty = Property()
            currProperty.setAddress(self.parseURLAddress(url))
            currProperty.setAddress(self.parseUrlID(url))
            fullURL = "https://www.daft.ie{}".format(url)
            currProperty.setURL(fullURL)
            resp = requests.get(fullURL)
            soup = BeautifulSoup(resp.content, 'html.parser')
            if resp.status_code == 200:
                priceDivTags = soup.find("div", attrs={'class' : priceRegex}).findChildren()
                for child in priceDivTags:
                    propertyPrice = self.parsePrice("".join(child.contents))
                    currProperty.setPrice(propertyPrice[0])
                    currProperty.setInterval(propertyPrice[1])
                roomInfoTag = soup.find("div", attrs={'class' : roomInfoRegex}).findChildren()
                for child in roomInfoTag:
                    if child['data-testid'] == '':
                        continue
                    elif child['data-testid'] == 'beds':
                        currProperty.setRoomType(child.text)
                    elif child['data-testid'] == 'baths':
                        currProperty.setBathroom(child.text)
                    elif child['data-testid'] == 'property-type':
                        currProperty.setPropertyType(child.text)
                overviewLists = soup.find("ul", attrs={'class': overViewRegex}).findChildren()
                for child in overviewLists:
                    if child.name =="li":
                        rawText = child.text.replace(" ", "")
                        rawData = rawText.split(":")
                        title = rawData[0]
                        data = rawData[1]
                        if title == "BedroomsAvailable":
                            currProperty.setNumBedrooms(int(re.sub('[^0-9]','', data)))
                        elif title == "AvailableFrom":
                            currProperty.setStartDate(data)
                        elif title == "AvailableFor":
                            currProperty.setDuration(data)
                        elif title == "Sharingwith":
                            currProperty.setSharing(int(re.sub('[^0-9]','', data)))
                        elif title == "OwnerOccupied":
                            currProperty.setOccupied(self.setOwnerOccupied(data))
                        elif title == "Preferences":
                            currProperty.setPreferences(data)
                        else:
                            print("Unknown Preferences!")
                description = soup.find("div", attrs={'data-testid': "description"}).text
                currProperty.setDescription(self.cleanDescription(description))
                
                

                
    

### DRIVER CODE
parser = PropertyParser("dublin", 500, 1000)
parser.pingDaft()

### sample json object to store in database..





        

