
"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS564 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import dump, loads
from re import sub

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'


"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon


"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]


"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""
def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)


def add_escape_quotes(row):
    for j in row.keys():
        if isinstance(row[j], str) and "\"" in row[j]:
            t = "\""
            for k in row[j]:
                if k != "\"":
                    t += k
                else:
                    t += "\"" + k
            t += "\""
            row[j] = t


def parseJson(json_file):
    # Lists of dictaionaries
    # users = load_pkl('users.pkl')
    # bids = load_pkl('bids.pkl')
    # items = load_pkl('items.pkl')
    # categories = load_pkl('categories.pkl')

    users = []
    bids = []
    items = []
    categories = {}

    # print('--- INFO ---- ', 'USERS: ',len(users), 'BIDS: ', len(bids),'ITEMS: ', len(items))

    # All info stored in these lists and the one dict
    with open(json_file, 'r') as f:
        json_items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file
        print(len(json_items))
        l = int(len(json_items))
        for i in range(l):
            curr = json_items[i]
            getUsers(curr, users)
            getBids(curr, bids)
            getItem(curr, items)
            getCategories(curr, categories)
    
   
    categoriesList = list(categories.keys())

    s = ''
    for item in users:
        line = ''
        for vals in item.values():
            line += str(vals) + '|'
        s += line[:-1] + '\n'
    s = s.strip()
    f = open("users.dat", "aw")
    f.write(s)
    f.close()

    s = ''
    for item in items:
        line = ''
        for vals in item.values():
            line += str(vals) + '|'
        s += line[:-1] + '\n'
    s = s.strip()
    f = open("items.dat", "aw")
    f.write(s)
    f.close()

    s = ''
    for item in bids:
        line = ''
        for vals in item.values():
            line += str(vals) + '|'
        s += line[:-1] + '\n'
    s = s.strip()
    f = open("bids.dat", "aw")
    f.write(s)
    f.close()

    s = '\n'.join(categoriesList)
    # for item in categories:
    #     line += str(items) + '|'
    #     s += line[:-1] + '\n'
    # s = s.strip()
    f = open("categories.dat", "aw")
    f.write(s)
    f.close()
        

def getCategories(current, categories):
    """
    We can either create the categories distinct entries with python or when inserting into database
    For now, just going to add all categories to dict and get rid of duplicates

    *** index the categories
    """
    categList = current['Category']
    for item in categList:
        if item not in categories:
            categories[str(item)] = 0


def getItem(current, items):
    # Need categories still
    temp_dict = {}
    temp_dict['ItemID'] = current['ItemID']
    temp_dict['Name'] = current['Name']
    categories = current['Category']
    temp_dict['Num_Categories'] = len(categories)
    temp_dict['Categories'] = ''
    for c in categories:
        temp_dict['Categories'] += c + ","
    temp_dict['Categories'] = temp_dict['Categories'][:-1]
    temp_dict['Currently'] = transformDollar(current['Currently'])
    if('Buy_Price' not in current.keys()):
        temp_dict['BuyPrice'] = "NULL"
    else:
        temp_dict['BuyPrice'] = transformDollar(current['Buy_Price'])
    temp_dict['FirstBid'] = transformDollar(current['First_Bid'])
    temp_dict['NumberBids'] = current['Number_of_Bids']
    temp_dict['Started'] = transformDttm(current['Started'])
    temp_dict['Ends'] = transformDttm(current['Ends'])
    temp_dict['SellerID'] = current['Seller']['UserID']
    temp_dict['Description'] = current['Description']
    add_escape_quotes(temp_dict)
    items.append(temp_dict)


def getBids(current, bids):
    """ Updates bids list which is passed to it and processes current
    in the bids 4 fields required: itemID, time, amount, userID.

    ** check for accuracy plz
    """
    bidList = current['Bids']
    
    if (bidList != None):
        for bid in bidList:
            temp_dict = {}
            temp_dict['Time'] = transformDttm(bid['Bid']['Time'])
            temp_dict['Amount'] = transformDollar(bid['Bid']['Amount'])
            temp_dict['userId'] = bid['Bid']['Bidder']['UserID']
            temp_dict['itemId'] = current['ItemID']
            add_escape_quotes(temp_dict)
            bids.append(temp_dict)            
        

def getUsers(current, usersList):
    """ Updates userList which is passed to it and processes current
        In each item processed there are two ways to discover users. Users can be sellers 
        and users can be found through the bids section. Duplicates not included.
    """

    # Add all bidders to usersList
    if (current['Bids'] != None):
        u = destructureBidders(current['Bids'])
        # Add users only if not already in usersList
        for i in u:
            add_escape_quotes(i) 
            matchFound = False
            for j in usersList:
                if i["UserID"] == j["UserID"]:
                    matchFound = True
            if not matchFound:                       
                usersList.append(i)

    # Add seller to usersList
    if (current['Seller'] != None):
        user = current['Seller']
        user['Location'] = current['Location']
        user['Country'] = current['Country']
        add_escape_quotes(user)

        # Add user only if not already in usersList
        matchFound = False
        for j in usersList:
            if user["UserID"] == j["UserID"]:
                matchFound = True
        if not matchFound: 
            usersList.append(user)


def destructureBidders(bids):
    bidders = []
    for bid in bids:
        if 'Location' not in bid['Bid']['Bidder'].keys():
            bid['Bid']['Bidder']['Location'] = "NULL"
        if 'Country' not in bid['Bid']['Bidder'].keys():
            bid['Bid']['Bidder']['Country'] = "NULL"
        bidders.append(bid['Bid']['Bidder'])
    return bidders


"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print("Success parsing " + f)


if __name__ == '__main__':
    main(sys.argv)
