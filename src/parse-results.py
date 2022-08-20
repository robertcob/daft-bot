

# get the payload
from requests import request

testURL = "https://www.daft.ie/sharing/dublin-city?rentalPrice_from=500&rentalPrice_to=1000&sort=publishDateDesc"
print(request.get(testURL))