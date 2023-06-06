import psycopg2
from . import runtime_data as RuntimeData


# connection to database which is running locally on the pi
# error handling is made via exceptions


# finds the element in _list
def find(element, _list):
    for i in range(len(_list)):
        if element == _list[i].beverage_id:
            return _list[i]
    return None


# returns true if _element is in _list
def is_in_list(_element, _list):
    for i in range(len(_list)):
        if _element == _list[i].beverage_id:
            return True
    return False


# returns true if the Beverage _needed is mixable with the current hopper configuration
# false if not
def mixable(_needed, _beverages):
    for i in range(len(_needed)):
        if not is_in_list(_needed[i], _beverages):
            return False
    return True


db_con = None
txn = None
connected = False


# sets up the connection to the database
def __init__():
    global db_con
    global txn
    global connected

    try:
        db_con = psycopg2.connect(
            host="localhost",
            database="siegmadb",
            user="admin",
            password="admin",
            port="5432",
        )

        if db_con is not None:
            connected = True

        txn = db_con.cursor()
        db_con.autocommit = False

    except (Exception, psycopg2.DatabaseError) as error:
        connected = False
        raise error


#################
# close_connection
#################
def close_connection():
    global connected
    global db_con

    if connected:
        try:
            txn.close()
            db_con.close()
        except Exception as error:
            raise error
    else:
        raise Exception("no connection to database given")


############
# commit
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
# send_query
###########
def send_query(query: str):
    global connected
    global txn

    if not connected:  # no connection given
        raise Exception("no connection to database given")

    try:  # connection is given
        txn.execute(query)
        res = txn.fetchall()
        return res

    except Exception as error:
        raise error


def send_update(query: str):
    global connected
    global txn

    if not connected:  # no connection given
        raise Exception("no connection to database given")

    try:  # connection is given
        txn.execute(query)

    except Exception as error:
        raise error


# exchanges the ingredients in the database
def changeBeverageOnHopper(currentID: int, toChangeID: int, hopperid: int):
    global connected
    global txn

    try:
        if currentID != -1:
            send_update(
                f"update Beverage set hopper_id = NULL where drink_to_add_id = {currentID} and hopper_id = {hopperid};"
            )
        if toChangeID != -1:
            send_update(
                f"update Beverage set hopper_id = {hopperid} where drink_to_add_id = {toChangeID}"
            )
        commit()
    except Exception as error:
        raise error


# returns all ingredients which are currently not on a hopper
def getAllOtherBeverages():
    global connected
    global txn

    try:
        result = []
        # return send_query('(select distinct name from is_mix_drink as m, recipe as r where m.drink_to_add_id = r.mixeddrinkid and r.beverageid in (select drink_to_add_id from Beverage where hopper_id is not null)) union (select name from Beverage where hopper_id is not null) order by name asc;')
        beveragesRes = send_query(
            "select drink_to_add_id, hopper_id, name, flow_speed from Beverage where hopper_id is null;"
        )
        for i in range(len(beveragesRes)):
            temp = RuntimeData.Beverage(
                beveragesRes[i][0],
                beveragesRes[i][1],
                beveragesRes[i][2],
                beveragesRes[i][3],
            )
            result.append(temp)
        return result

    except Exception as error:
        raise error


# returns all ingredients which are currently on a hopper
def getAllAvailableBeverages():
    global connected
    global txn

    try:
        result = []
        # return send_query('(select distinct name from is_mix_drink as m, recipe as r where m.drink_to_add_id = r.mixeddrinkid and r.beverageid in (select drink_to_add_id from Beverage where hopper_id is not null)) union (select name from Beverage where hopper_id is not null) order by name asc;')
        beveragesRes = send_query(
            "select drink_to_add_id, hopper_id, name, flow_speed from Beverage where hopper_id is not null order by hopper_id asc;"
        )
        for i in range(len(beveragesRes)):
            temp = RuntimeData.Beverage(
                beveragesRes[i][0],
                beveragesRes[i][1],
                beveragesRes[i][2],
                beveragesRes[i][3],
            )
            result.append(temp)
        return result

    except Exception as error:
        raise error


# returns a list of all the needed ingredients for a mix_drink
def getNeededBeverages(needed, allbeverages):
    # there are only ids in needed
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
        allMixedDrinksRes = send_query(
            "select m.drink_to_add_id, m.name, r.beverageid, r.fillingamount from is_mix_drink as m, recipe as r where m.drink_to_add_id = r.mixeddrinkid;"
        )
        if len(allMixedDrinksRes) == 0:
            return result

        needed = []
        fillamounts = []
        currentID = allMixedDrinksRes[0][0]
        currentName = allMixedDrinksRes[0][1]
        # loop through all possible mixed drinks
        for i in range(len(allMixedDrinksRes)):
            # get all the needed ingredients
            if currentID != allMixedDrinksRes[i][0]:  # new mixed drink
                # we got all the ids for the needed drinks
                temp = getNeededBeverages(needed, allGivenBeverages)
                if temp != []:  # drink is mixable
                    result.append(
                        RuntimeData.MixDrinkInformation(
                            currentID, currentName, temp, fillamounts
                        )
                    )
                needed = []
                fillamounts = []

            needed.append(allMixedDrinksRes[i][2])
            fillamounts.append([allMixedDrinksRes[i][2], allMixedDrinksRes[i][3]])
            currentID = allMixedDrinksRes[i][0]
            currentName = allMixedDrinksRes[i][1]

        # one last time so everything gets checked
        tempLast = getNeededBeverages(needed, allGivenBeverages)
        if tempLast != []:
            result.append(
                RuntimeData.MixDrinkInformation(currentID, currentName, tempLast, fillamounts)
            )
        return result

    except Exception as error:
        raise error


# returns a list of all mixeddrinks stored in the database as a list of mix_drink_information objects
def getAllMixedDrinks() -> list[RuntimeData.MixDrinkInformation]:
    global connected
    global txn

    try:
        result = []
        mixeddrinks = send_query("select drink_to_add_id, name from is_mix_drink")

        for mixeddrink in mixeddrinks:
            drink = RuntimeData.MixDrinkInformation(mixeddrink[0], mixeddrink[1], [], [])
            res = send_query(
                f"select beverageid, fillingamount from recipe where mixeddrinkid = {mixeddrink[0]}"
            )
            for r in res:
                b = send_query(
                    f"select drink_to_add_id, hopper_id, name, flow_speed from Beverage where drink_to_add_id = {r[0]}"
                )
                beverage = b[0]
                drink.mix_drink_needed_beverages.append(
                    RuntimeData.Beverage(beverage[0], beverage[1], beverage[2], beverage[3])
                )
                drink.mix_drink_fill_perc_beverages.append((beverage[0], r[1]))
            result.append(drink)

        return result

    except Exception as error:
        raise error


# checks if a mix_drink with the given already exists in the database
def isNameAvailable(__name: str):
    res = send_query(f"select name from is_mix_drink where name = '{__name}';")
    return len(res) == 0


# inserts the given cocktail into the database
def saveCocktails(toSave: RuntimeData.MixDrinkInformation):
    global connected
    global txn

    try:
        # insert new mix_drink into mixeddrinks table
        if isNameAvailable(toSave.mix_drink_name):
            # insert new mix_drink and get the given drink_to_add_id
            res = send_query(
                f"insert into is_mix_drink(name) values('{toSave.mix_drink_name}') returning drink_to_add_id;"
            )
            # insert recipe
            for i in range(len(toSave.mix_drink_needed_beverages)):
                send_update(
                    f"insert into recipe(beverageid, mixeddrinkid, fillingamount) values({toSave.mix_drink_needed_beverages[i].beverage_id}, {res[0][0]}, {toSave.get_fill_perc(toSave.mix_drink_needed_beverages[i].beverage_id)});"
                )
            # commit the changes
            commit()
            return True
        else:
            return False
    except Exception as error:
        raise error
