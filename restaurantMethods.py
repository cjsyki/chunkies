#takes yelp json and returns name of restaurant
def returnName(dictionary):
    return dictionary["name"]

#returns coordinates array
def returnCoordinates(dictionary):
    return [dictionary["coordinates"]["latitude"], dictionary["coordinates"]["longitude"]]

#returns address
def returnAddress(dictionary):
    return dictionary["location"]["display_address"]

#returns categories
def returnCategories(dictionary):
    retArray = []
    for category in dictionary["categories"]:
        retArray.append(category["alias"])
    return retArray

#returns price
def returnPrice(dictionary):
    return dictionary["price"]