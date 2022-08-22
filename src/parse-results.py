import requests
from bs4 import BeautifulSoup
import re

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
            [print(link['href']) for link in content if re.match(propertysURLRegex, link['href'])]

    def getDiff(self, currPropertyURLs):
        prevPropertURLs
        return prevPropertURLs - currPropertyURLs

    def exportProperties(self, newPropetyURLs):

        
### DRIVER CODE
parser = PropertyParser("dublin", 500, 1000)
parser.pingDaft()



        

