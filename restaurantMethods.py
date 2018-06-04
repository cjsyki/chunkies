import random
from yelp import SEARCH_LIMIT

# generates an array from 1 to length of parameter,
# shuffes that array 10000 times,
# and sorts parameter according to the indices of array
def generateRandomList(array):
    length = len(array)
    baseArray = list(range(0, length))
    for i in range(0, 10000):
        a = random.randrange(0, length)
        b = random.randrange(0, length)
        while a == b:
            b = random.randrange(0, length)
        baseArray[a], baseArray[b] = baseArray[b], baseArray[a]
    for i in range(0,length):
        array[i], array[baseArray[i]] = array[baseArray[i]], array[i]
    return array


arary = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','w','x','y','z']

print(generateRandomList(arary))