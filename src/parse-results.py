import requests
from bs4 import BeautifulSoup
import re

global CurrProperties
class Property:
    def __init__(self, price, address, url, roomType) -> None:
        self.price = price
        self.address = address
        self.url = url
        self.roomType = roomType

class PropertyParser:
    def __init__(self, location, priceFrom, priceTo) -> None:
        self.priceFrom = str(priceFrom)
        self.priceTo = str(priceTo)
        self.location = str(location)
        self.newProperties = []

    # def pingDaft(self):
    #     pingURL = "https://www.daft.ie/sharing/{}?rentalPrice_from={}&rentalPrice_to={}&sort=publishDateDesc".format(self.location, self.priceFrom, self.priceTo)
    #     resp = requests.get(pingURL)
    #     innerRegexs = [re.compile("^TitleBlock__CardInfoItem"), re.compile("^TitleBlock__Address"),  re.compile("^TitleBlock__Price") ]
    #     propertysRegex = re.compile("^SearchPage__Result")
    #     if resp.status_code == 200:
    #         html_doc = resp.content
    #         soup = BeautifulSoup(html_doc, 'html.parser')
    #         content = soup.find_all("li", propertysRegex)
    #         for room in content:
    #             details = {}
    #             room = BeautifulSoup(str(room))
    #             propertyURL = room.find("a")
    #             details['url'] = propertyURL['href']
    #             raw = []
    #             for re in innerRegexs:
    #                 raw.append(room.find_all("div", attrs={'class' : re}))
    #                 raw.append(room.find_all("p", attrs={'class' : re}))
    #             for rawdetails in raw:
    #                 if details.text != "":
    #                     pass

    ### returns url of all current rental rooms in duration
    def pingDaft(self):
        pingURL = "https://www.daft.ie/sharing/{}?rentalPrice_from={}&rentalPrice_to={}&sort=publishDateDesc".format(self.location, self.priceFrom, self.priceTo)
        resp = requests.get(pingURL)
        propertysURLRegex = re.compile("^/share")
        if resp.status_code == 200:
            html_doc = resp.content
            soup = BeautifulSoup(html_doc, 'html.parser')
            content = soup.find_all("a", href=True)
            diff = self.getDiff([link['href'] for link in content if re.match(propertysURLRegex, link['href'])])
            if len(diff) > 0:
                self.exportProperties(diff)
        else:
            print("bad daft url!")

    def getDiff(self, currPropertyURLs):
        prevPropertURLs = CurrProperties
        CurrProperties = currPropertyURLs
        return prevPropertURLs - currPropertyURLs

    def exportProperties(self, newPropetyURLs):
        priceRegex = re.compile("^TitleBlock__Price")
        addressRegex = re.compile("^TitleBlock__Address")
        roomInfoRegex = re.compile("^TitleBlock__CardInfo")
        for url in newPropetyURLs:
            resp = requests.get("https://www.daft.ie{}".format(url))
            soup = BeautifulSoup(resp, 'html.parser')
            if resp.status_code == 200:
                priceDiv = soup.find("div", attrs={'class' : priceRegex})
                roomInfoTag = soup.find("div", attrs={'class' : roomInfoRegex}).findChildren
                for child in roomInfoTag:
                    if child['data-testid'] == '':
                        continue
                    elif child['data-testid'] == 'beds':
                        bedType = child.text
                    elif child['data-testid'] == 'baths':
                        bathType = child.text
                    elif child['data-testid'] == 'property-type':
                        propertyType = child.text

                address = soup.find("h1", attrs={'class' : addressRegex}).text
                price = priceDiv.findChild().text
                continue



        
### DRIVER CODE
parser = PropertyParser("dublin", 500, 1000)
parser.pingDaft()



        

