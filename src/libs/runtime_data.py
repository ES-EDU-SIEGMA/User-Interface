## beverage
#   one object displays one tupel from in the database from the table beverage
class Beverage:
    ## id of the hopper the beverage is in, None if its not in the machine
    m_hopperid: int
    ## name of the beverage
    m_name: str
    ## id from database tupel
    m_id: int
    ## flowspeed of the beverage
    m_flowspeed: int

    ## constructor
    def __init__(self, __id: int, __hopperid: int, __name: str, __flowspeed: int):
        self.m_hopperid = __hopperid
        self.m_id = __id
        self.m_name = __name
        self.m_flowspeed = __flowspeed

    ## to string
    def __str__(self):
        return f"[{self.m_name}, {self.m_id}]"


## mixDrinkInformation
#   represents the mixdrink
#   it stores the bevereages needed to mix the drink and all the other necessarry information
class MixDrinkInformation:
    ## list of all the needed beverages (stores objects of the datatype beverage)
    m_neededBeverages = []  # type: beverage
    ## list of the corresponding fillpercenteges, its a list in the list e.g. [[1,23], [2, 77]] where [x][0] is the id of the beverage and [x][1] is the fillpercentage
    m_fillpercToBvg = []  # type: int
    ## name of the drink
    m_name: str
    ## id of the mixdrink, comes from the table mixdrinks
    m_id: int

    ## constructor
    def __init__(self, __id, __name, __neededBeverages, __fillpercToBvg):
        self.m_neededBeverages = __neededBeverages
        self.m_name = __name
        self.m_id = __id
        self.m_fillpercToBvg = __fillpercToBvg

    ## returns the fillpercentage to the given id
    def getFillPercToId(self, __id: int) -> int:
        for i in range(len(self.m_fillpercToBvg)):
            if __id == self.m_fillpercToBvg[i][0]:
                return self.m_fillpercToBvg[i][1]

    ## set the fillpercentage to the given id
    def setFillPercToId(self, __id: int, __perc: int):
        for i in range(len(self.m_fillpercToBvg)):
            if __id == self.m_fillpercToBvg[i][0]:
                self.m_fillpercToBvg[i][1] = __perc

    def __str__(self):
        return f"{self.m_name}, {self.m_id}"


## runtimeData
#   combines everything into one object
class RuntimeData:
    ## list of all beverages currently on the machine
    m_beverageList = None
    ## list of all mixdrinks which are currently mixable
    m_mixeddrinkList = None

    def __init__(self, __beverageList, __mixeddrinkList):
        self.m_beverageList = __beverageList
        self.m_mixeddrinkList = __mixeddrinkList

    ## getMixedDrinkToId
    # find the mixdrink to the given id
    #
    # PARAMS:
    #   _id: id of the element to be searched for
    #
    # RETURNS None if the mixeddrink is not in the list, else the object
    def getMixedDrinkToId(self, _id: int):
        for i in range(len(self.m_mixeddrinkList)):
            if _id == self.m_mixeddrinkList[i].m_id:
                return self.m_mixeddrinkList[i]
        return None

    ## getBeverageToId
    #
    # see: getMixedDrinkToId
    def getBeverageToId(self, _id: int):
        for i in range(len(self.m_beverageList)):
            if _id == self.m_beverageList[i].m_id:
                return self.m_beverageList[i]
        return None
