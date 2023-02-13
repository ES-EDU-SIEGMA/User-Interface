import psycopg2
import runtimeData as rtd
#connection to databse which is running locally on the pi
#error handling is made via exceptions

# finds the element in _list
def find(element, _list):
    for i in range(len(_list)):
        if element == _list[i].m_id:
            return _list[i]
    return None

# returns true if _element is in _list
def isInList(_element, _list):
    for i in range(len(_list)):
        if _element == _list[i].m_id:
            return True
    return False

# returns true if the beverage _needed is mixable with the current hopper configuration
# false if not
def mixable(_needed, _beverages):
    for i in range(len(_needed)):
        if not isInList(_needed[i], _beverages):
            return False
    return True

db_con = None
txn = None
connected = False

## sets up the connection to the database
def __init__():
    global db_con
    global txn
    global connected
    
    try:
        db_con = psycopg2.connect(
            host='localhost',
            database='drinkmixingmachine',
            user='admin',
            password='admin',
            port = '5432'
        )
        
        if db_con is not None:
            connected = True
        
        txn = db_con.cursor()
        db_con.autocommit = False

    except (Exception, psycopg2.DatabaseError) as error:
        connected = False
        raise error

#################
#close_connection
#################
def close_connection():
    global connected
    global db_con
    
    if connected:
        try:
            txn.close()
            db_con.close()
            print("connection closed successfully")
        except Exception as error:
            raise error
    else:
        raise Exception("no connection to database given")

############
#commit
#############
def commit():
    global connected
    global txn
    global db_con
    
    if not connected:
        raise Exception("no connection to database given")
            
    try:
        db_con.commit()
    except Exception as error:
        raise error

############
#send_query
###########
def send_query(query : str):
    global connected
    global txn
    
    if not connected: #no connection given
        raise Exception("no connection to database given")   
    
    try: #connection is given
        txn.execute(query)
        res = txn.fetchall()
        return res
        
    except Exception as error:
        raise error

def send_update(query : str):
    global connected
    global txn
    
    if not connected: #no connection given
        raise Exception("no connection to database given")   
    
    try: #connection is given
        txn.execute(query)

    except Exception as error:
        raise error

# exchanges the beverages in the database
def changeBeverageOnHopper(currentID : int, toChangeID : int, hopperid : int):
    global connected
    global txn

    try:
        if currentID != -1:
            send_update(f'update beverage set hopperid = NULL where id = {currentID} and hopperid = {hopperid};')
        if toChangeID != -1:
            send_update(f'update beverage set hopperid = {hopperid} where id = {toChangeID}')
        commit()
    except Exception as error:
        raise error 

# returns all beverages which are currently not on a hopper
def getAllOtherBeverages():
    global connected
    global txn
    
    try:
        result = []
        #return send_query('(select distinct name from mixeddrink as m, recipe as r where m.id = r.mixeddrinkid and r.beverageid in (select id from beverage where hopperid is not null)) union (select name from beverage where hopperid is not null) order by name asc;')
        beveragesRes = send_query('select id, hopperid, name, flowspeed from beverage where hopperid is null;')
        for i in range(len(beveragesRes)):
            temp = rtd.beverage(beveragesRes[i][0], beveragesRes[i][1], beveragesRes[i][2], beveragesRes[i][3])
            result.append(temp)
        return result
            
    except Exception as error:
        raise error

# returns all beverages which are currently on a hopper
def getAllAvailableBeverages():
    global connected
    global txn
    
    try:
        result = []
        #return send_query('(select distinct name from mixeddrink as m, recipe as r where m.id = r.mixeddrinkid and r.beverageid in (select id from beverage where hopperid is not null)) union (select name from beverage where hopperid is not null) order by name asc;')
        beveragesRes = send_query('select id, hopperid, name, flowspeed from beverage where hopperid is not null order by hopperid asc;')
        for i in range(len(beveragesRes)):
            temp = rtd.beverage(beveragesRes[i][0], beveragesRes[i][1], beveragesRes[i][2], beveragesRes[i][3])
            result.append(temp)
        return result
            
    except Exception as error:
        raise error

# returns a list of all the needed beverages for a mixdrink
def getNeededBeverages(needed, allbeverages):
    #there are only ids in needed
    res = []
    if not mixable(needed, allbeverages):
        return []
    for i in range(len(needed)):
        temp = find(needed[i], allbeverages)
        res.append(temp)
    return res
        
# returns a list of all mixable mixdrinks with the current hopper configuration
def getAllAvailableMixedDrinks():
    global connected
    global txn
    
    try:
        result = []
        
        allGivenBeverages = getAllAvailableBeverages()
        allMixedDrinksRes = send_query('select m.id, m.name, r.beverageid, r.fillingamount from mixeddrink as m, recipe as r where m.id = r.mixeddrinkid;')
        
        needed = []
        fillamounts = []
        currentID = allMixedDrinksRes[0][0]
        currentName = allMixedDrinksRes[0][1]
        #loop through all possible mixed drinks
        for i in range(len(allMixedDrinksRes)):
            #get all the needed beverages
            if currentID != allMixedDrinksRes[i][0]: # new mixed drink
                #we got all the ids for the needed drinks
                temp = getNeededBeverages(needed, allGivenBeverages)
                if temp != []: #drink is mixable
                    result.append(rtd.mixDrinkInformation(currentID, currentName, temp, fillamounts))
                needed = []
                fillamounts = []
            
            needed.append(allMixedDrinksRes[i][2])
            fillamounts.append([allMixedDrinksRes[i][2], allMixedDrinksRes[i][3]])
            currentID = allMixedDrinksRes[i][0]
            currentName = allMixedDrinksRes[i][1]
        
        #one last time so everything gets checked
        tempLast = getNeededBeverages(needed, allGivenBeverages)
        if tempLast != []:
            result.append(rtd.mixDrinkInformation(currentID, currentName, tempLast, fillamounts))
        return result
            
    except Exception as error:
        raise error

# returns a list of all mixeddrinks stored in the database as a list of mixDrinkInformation objects
def getAllMixedDrinks() -> list[rtd.mixDrinkInformation]:
    global connected
    global txn
    
    try:
        result = []
        mixeddrinks = send_query("select id, name from mixeddrink")

        for mixeddrink in mixeddrinks:
            drink = rtd.mixDrinkInformation(mixeddrink[0],mixeddrink[1],[],[])
            res = send_query(f"select beverageid, fillingamount from recipe where mixeddrinkid = {mixeddrink[0]}")
            for r in res:
                b = send_query(f"select id, hopperid, name, flowspeed from beverage where id = {r[0]}")
                beverage = b[0]
                drink.m_neededBeverages.append(rtd.beverage(beverage[0], beverage[1], beverage[2], beverage[3]))
                drink.m_fillpercToBvg.append((beverage[0], r[1]))
            result.append(drink)

        return result
            
    except Exception as error:
        raise error

# checks if a mixdrink with the given already exists in the database
def isNameAvailable(__name : str):
    res = send_query(f"select name from mixeddrink where name = '{__name}';")
    return len(res) == 0

# inserts the given cocktail into the database
def saveCocktails(toSave : rtd.mixDrinkInformation):
    global connected
    global txn
    
    try:
        #insert new mixdrink into mixeddrinks table
        if isNameAvailable(toSave.m_name):
            #insert new mixdrink and get the given id
            res = send_query(f"insert into mixeddrink(name) values('{toSave.m_name}') returning id;")
            #insert recipe
            for  i in range(len(toSave.m_neededBeverages)):
                send_update(f"insert into recipe(beverageid, mixeddrinkid, fillingamount) values({toSave.m_neededBeverages[i].m_id}, {res[0][0]}, {toSave.getFillPercToId(toSave.m_neededBeverages[i].m_id)});")
            #commit the changes
            commit()
            return True
        else:
            return False
    except Exception as error:
        raise error