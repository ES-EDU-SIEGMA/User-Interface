import psycopg2
from . import runtime_data as rtd


# connection to databse which is running locally on the pi
# error handling is made via exceptions


# finds the element in _list
def find(element, _list):
    for i in range(len(_list)):
        if element == _list[i].m_id:
            return _list[i]
    return None


# returns true if _element is in _list
def is_in_list(_element, _list):
    for i in range(len(_list)):
        if _element == _list[i].m_id:
            return True
    return False


# returns true if the beverage _needed is mixable with the current hopper configuration
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
            database="drinkmixingmachine",
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


# exchanges the beverages in the database
def change_beverage_on_hopper(current_id: int, to_change_id: int, hopper_id: int):
    global connected
    global txn

    try:
        if current_id != -1:
            send_update(
                f"update beverage set hopperid = NULL where id = {current_id} and hopperid = {hopper_id};"
            )
        if to_change_id != -1:
            send_update(
                f"update beverage set hopperid = {hopper_id} where id = {to_change_id}"
            )
        commit()
    except Exception as error:
        raise error


# returns all beverages which are currently not on a hopper
def get_all_other_beverages():
    global connected
    global txn

    try:
        result = []
        # return send_query('(select distinct name from mixeddrink as m, recipe as r where m.id = r.mixeddrinkid and r.beverageid in (select id from beverage where hopperid is not null)) union (select name from beverage where hopperid is not null) order by name asc;')
        beveragesRes = send_query(
            "select id, hopperid, name, flowspeed from beverage where hopperid is null;"
        )
        for i in range(len(beveragesRes)):
            temp = rtd.beverage(
                beveragesRes[i][0],
                beveragesRes[i][1],
                beveragesRes[i][2],
                beveragesRes[i][3],
            )
            result.append(temp)
        return result

    except Exception as error:
        raise error


# returns all beverages which are currently on a hopper
def get_all_available_beverages():
    global connected
    global txn

    try:
        result = []
        # return send_query('(select distinct name from mixeddrink as m, recipe as r where m.id = r.mixeddrinkid and r.beverageid in (select id from beverage where hopperid is not null)) union (select name from beverage where hopperid is not null) order by name asc;')
        beveragesRes = send_query(
            "select id, hopperid, name, flowspeed from beverage where hopperid is not null order by hopperid asc;"
        )
        for i in range(len(beveragesRes)):
            temp = rtd.beverage(
                beveragesRes[i][0],
                beveragesRes[i][1],
                beveragesRes[i][2],
                beveragesRes[i][3],
            )
            result.append(temp)
        return result

    except Exception as error:
        raise error


# returns a list of all the needed beverages for a mixdrink
def get_needed_beverages(needed, all_beverages):
    # there are only ids in needed
    res = []
    if not mixable(needed, all_beverages):
        return []
    for i in range(len(needed)):
        temp = find(needed[i], all_beverages)
        res.append(temp)
    return res


# returns a list of all mixable mixdrinks with the current hopper configuration
def get_all_available_mixed_drinks():
    global connected
    global txn

    try:
        result = []

        allGivenBeverages = get_all_available_beverages()
        allMixedDrinksRes = send_query(
            "select m.id, m.name, r.beverageid, r.fillingamount from mixeddrink as m, recipe as r where m.id = r.mixeddrinkid;"
        )
        if len(allMixedDrinksRes) == 0:
            return result

        needed = []
        fillamounts = []
        currentID = allMixedDrinksRes[0][0]
        currentName = allMixedDrinksRes[0][1]
        # loop through all possible mixed drinks
        for i in range(len(allMixedDrinksRes)):
            # get all the needed beverages
            if currentID != allMixedDrinksRes[i][0]:  # new mixed drink
                # we got all the ids for the needed drinks
                temp = get_needed_beverages(needed, allGivenBeverages)
                if temp != []:  # drink is mixable
                    result.append(
                        rtd.mixDrinkInformation(
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
        tempLast = get_needed_beverages(needed, allGivenBeverages)
        if tempLast != []:
            result.append(
                rtd.mixDrinkInformation(currentID, currentName, tempLast, fillamounts)
            )
        return result

    except Exception as error:
        raise error


# returns a list of all mixeddrinks stored in the database as a list of mixDrinkInformation objects
def get_all_mixed_drinks() -> list[rtd.MixDrinkInformation]:
    global connected
    global txn

    try:
        result = []
        mixeddrinks = send_query("select id, name from mixeddrink")

        for mixeddrink in mixeddrinks:
            drink = rtd.mixDrinkInformation(mixeddrink[0], mixeddrink[1], [], [])
            res = send_query(
                f"select beverageid, fillingamount from recipe where mixeddrinkid = {mixeddrink[0]}"
            )
            for r in res:
                b = send_query(
                    f"select id, hopperid, name, flowspeed from beverage where id = {r[0]}"
                )
                beverage = b[0]
                drink.m_needed_beverages.append(
                    rtd.beverage(beverage[0], beverage[1], beverage[2], beverage[3])
                )
                drink.m_fill_percentage_to_beverage.append((beverage[0], r[1]))
            result.append(drink)

        return result

    except Exception as error:
        raise error


# checks if a mixdrink with the given already exists in the database
def is_name_available(__name: str):
    res = send_query(f"select name from mixeddrink where name = '{__name}';")
    return len(res) == 0


# inserts the given cocktail into the database
def save_cocktails(to_save: rtd.MixDrinkInformation):
    global connected
    global txn

    try:
        # insert new mixdrink into mixeddrinks table
        if is_name_available(to_save.m_name):
            # insert new mixdrink and get the given id
            res = send_query(
                f"insert into mixeddrink(name) values('{to_save.m_name}') returning id;"
            )
            # insert recipe
            for i in range(len(to_save.m_needed_beverages)):
                send_update(
                    f"insert into recipe(beverageid, mixeddrinkid, fillingamount) values({to_save.m_needed_beverages[i].m_id}, {res[0][0]}, {to_save.get_fill_percentage_to_id(to_save.m_needed_beverages[i].m_id)});"
                )
            # commit the changes
            commit()
            return True
        else:
            return False
    except Exception as error:
        raise error
