import os
from daftlistings import Daft, Location, SearchType, SortType

class DaftListings:
    def __init__(self, location, lowPrice, highPrice, ownerOccupied) -> None:
        self.location = self.parseLocation(location)
        self.lowPrice = lowPrice
        self.highPrice = highPrice
        self.ownerOccupied = ownerOccupied
    
    def parseLocation(self, location):
        try:
            clean = location.lower()
            if clean == "dublin":
                self.location = Location.DUBLIN
            elif clean == "cork":
                self.location = Location.CORK
            elif clean == "galway":
                self.location = Location.GALWAY
            elif clean == "louth":
                self.location = Location.LOUTH
            elif clean == "meath":
                self.location = Location.MEATH
            elif clean == "kildare":
                self.location = Location.KILDARE
            elif clean == "wicklow":
                self.location = Location.WICKLOW
            return self.location
        except:
            print("failed to find location, tool only searches for Dublin, Cork, Galway, Wicklow, Louth, Meath and Kildare")

    def setListings(self):
        daft = Daft()
        daft.set_location(self.location)
        daft.set_search_type(SearchType.SHARING)
        daft.set_sort_type(SortType.PUBLISH_DATE_DESC)
        daft.set_owner_occupied(self.ownerOccupied)
        daft.set_min_price(self.lowPrice)
        daft.set_max_price(self.highPrice)
        return daft.search(1)
    
    def exportListings(self, listings):
        listingsToExport = []
        for property in listings:
            data =  {
                "_id": str(property.id), ##get from parsing the URL
                "url": property.daft_link,
                "price": property.monthly_price,
                "address": property.title,
                "extra": {
                    "agent_id" : property.agent_id,
                    "publish_date" : property.publish_date,
                    "bedrooms": property.bedrooms,
                    "property_type": property.category
                    }
                }
            listingsToExport.append(data)
        return listingsToExport

def inputOwnerOccupied():
    ownerOccupiedStatus = input("Search for properties that are Owner Occupied? yes or no ")
    lowerOOStatus = ownerOccupiedStatus.lower()
    if lowerOOStatus == "yes":
        return True
    else:
        return False
        
def executeDaft():
    email = input("Please enter email associated with daft account ")
    passkey = input("Please enter password associated with daft account ")
    os.environ['DAFTEMAIL'] = email
    os.environ['DAFTPASSWORD'] = passkey
    county = input("Please enter the county to search rooms for: ")
    priceLow = int(input("Please enter lowest room price: "))
    priceHigh = int(input("Please enter highest room price: "))
    ownerOccupiedStatus = inputOwnerOccupied()
    listings = DaftListings(county, priceLow, priceHigh, ownerOccupiedStatus)
    return listings