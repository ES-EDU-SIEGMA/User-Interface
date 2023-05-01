import json
import runtimeData as rtd


def getDrinkList():
    """ returns the drinkList.json file as a dict """

    try:
        with open("drinkList.json","r") as jsonFile:
            return json.load(jsonFile)
        
    except Exception as error:
        print(error)
        return []



def writeDrinkList(newDrinkList):
    """ writes the parameter of the function into the drinkList.json file """

    try:
        with open("drinkList.json","w") as jsonFile:
            json.dump(newDrinkList,jsonFile, indent=4)
    
    except Exception as error:
        print(error)



def getDrinksOnHopper():
    """ returns the IDs of all drinks on the hopper """

    drinkList = getDrinkList()
    result = []

    for drinkID in drinkList:
        if drinkList[drinkID]["hopperid"]!= None:
            result.append(drinkID)
    return result


""" #currently not used
def getDispensableDrinks():
    returns the IDs of all drinks that can be dispensed
    
    drinkList = getDrinkList()
    result = []

    for drinkID in drinkList:
        if drinkList[drinkID]["dispensable"] == True:
            result.append(drinkID)

    return result """



def determineDispensableDrinks():
    """ Changes the dispensable value of a drink depending on whether a drink is 
        dispensable. A drink is dispensable if all required drinks are on the hopper """

    drinkList = getDrinkList()
    drinkIDsOnHopper = [eval(i) for i in getDrinksOnHopper()]

    for drinkID in drinkList:

        drinkList[drinkID]["dispensable"] = False
        requiredDrinkIDs = list(list(zip(*drinkList[drinkID]["requiredDrinks"]))[0])
        # requiredDrinkIDs is a list of all required drinkIDs for a drink

        if(all(drink in drinkIDsOnHopper for drink in requiredDrinkIDs)):
        # tests whether the list of required drinkIDs is a subset of the list of drinkIDs on the hopper

            drinkList[drinkID]["dispensable"] = True

    writeDrinkList(drinkList)
    # updates the dispensable value for all drinks



def addDrink(mixdrink,id = None, name = None, requiredDrinks = [], flowspeed = None):
    """ Adds a new drink to the drinkList and determines wheter the drink can be dispensed"""

    drinkList = getDrinkList()
    drinkList[id]={"id":id,"name":name,"hopperid":None,"dispensable":False,"flowspeed":flowspeed,"mixdrink":mixdrink,"requiredDrinks":requiredDrinks}
    
    writeDrinkList(drinkList)
    determineDispensableDrinks()



def changeDrinkIDsOnHopper(hopperID, newDrinkOnHopperID):
    """ changes the hopperid for the given drinkID to the parameter hopperID and
        changes the hopperid for the previous drink on the hopper to None and
        determines which drinks are dispensable """
    
    drinkList = getDrinkList()

    for drinkID in drinkList:

        if drinkList[drinkID]["hopperid"] == hopperID:
            drinkList[drinkID]["hopperid"] = None
        # remove the old drink from the hopper by setting hopperid to None

        if drinkList[drinkID]["id"] == int(newDrinkOnHopperID):
            drinkList[drinkID]["hopperid"] = hopperID
        # update the hopperid for the new drink

    writeDrinkList(drinkList)
    determineDispensableDrinks()



def reformatJson():
    """ reformats the jsonfile after manually changing it for aesthetic purposes """

    drinks = getDrinkList()
    writeDrinkList(drinks)

















# Implementing SQL database with the new jsonFile in Json
# only functions that are called outside of dbcon are implemented


def createBevDrinkObject(drinkID):
    """ creates a beverage object from runtimeData """

    drinkList = getDrinkList()
    bevid = int(drinkID)
    bevhopperid = drinkList[str(drinkID)]["hopperid"]
    bevname = str(drinkList[str(drinkID)]["name"])
    bevflowspeed = int(drinkList[str(drinkID)]["flowspeed"])

    return rtd.beverage(bevid,bevhopperid,bevname,bevflowspeed)



def createMixDrinkObject(drink):
    """ creates a mixdrinkObject from runtimeData """

    drinkList = getDrinkList()
    currentID = int(drink["id"])
    currentName = str(drink["name"])
    fillamounts = drink["requiredDrinks"]
    temp = []

    for x in list(list(zip(*drinkList[str(currentID)]["requiredDrinks"]))[0]):
        temp.append(createBevDrinkObject(x))

    return rtd.mixDrinkInformation(currentID,currentName,temp,fillamounts)    



def getAllOtherBeverages():
    """ returns a list of beverage objects which are not on the hopper """
    drinkList = getDrinkList()
    bevresult = []

    for drinkID in drinkList:
        if (drinkList[drinkID]["hopperid"] == None) and (drinkList[drinkID]["mixdrink"] == False):
            bevresult.append(createBevDrinkObject(drinkID))

    return bevresult



def getAllAvailableBeverages():
    """ returns a list of beverage objects which are active on the hopper """

    drinkList = getDrinkList()
    bevresult = []

    for drinkID in drinkList:
        if (drinkList[drinkID]["hopperid"] != None) and (drinkList[drinkID]["mixdrink"] == False):
            bevresult.append(createBevDrinkObject(drinkID))

    return bevresult



def changeBeverageOnHopper(currentID : int, toChangeID : int, hopperID : int):
    """ allocates a new drink on the hopper by changing the hopperid """

    changeDrinkIDsOnHopper(hopperID,toChangeID)



def getAllAvailableMixedDrinks():
    """ returns a list of mixDrinkInformation objects
        consisting of all mixdrinks which can be mixed """

    drinkList = getDrinkList()
    dispensableMixDrinks = []

    for drinkID in drinkList:
        if (drinkList[drinkID]["mixdrink"] == True) and (drinkList[drinkID]["dispensable"] == True):
            dispensableMixDrinks.append(createMixDrinkObject(drinkList[drinkID]))
                
    return dispensableMixDrinks
    # create mixDrinkInformation object as a resut



def getAllMixedDrinks():
    """ returns a list of mixDrinkInformation objects
        consisting of all mixdrinks"""

    drinkList = getDrinkList()
    dispensableMixDrinks = []

    for drinkID in drinkList:
        if drinkList[drinkID]["mixdrink"] == True:
            dispensableMixDrinks.append(createMixDrinkObject(drinkList[drinkID]))
                
    return dispensableMixDrinks
    


def isNameAvailable(__name : str):
    """ checks whether a given name is allready used """

    drinkList = getDrinkList()
    nameFree = True

    for drinkID in drinkList:
        if drinkList[drinkID]["name"] == __name:
            nameFree = False
            break
    
    return nameFree
    


def saveCocktails(mixDrinkInformation : rtd.mixDrinkInformation):
    """ saves a new mixdrink to the drinkList """
    
    name = mixDrinkInformation.m_name

    if isNameAvailable(name):
        mixid = mixDrinkInformation.m_id
        mixname = mixDrinkInformation.m_name
        m_required = mixDrinkInformation.m_fillpercToBvg
        mixdrink = True

        if len(m_required)>1:
            mixdrink = False

        #(mixdrink,id = None, name = None, flowspeed = 0, requiredDrinks = [])
        addDrink(mixdrink,mixid,mixname,m_required)

    else:
        return False
    

def __init__():
    pass

def close_connection():
    pass
