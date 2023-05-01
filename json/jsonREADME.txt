All methods that call the database through the module "dbcon" are implemented in the module "jsonData"

The following modules call "dbcon":
siegma2223; newCocktailWindow; editHoppersWindow; createdCocktailsWindow

Steps to exchange the database for a jsonFile:
1. exchange import dbcon as xyz  to  import jsonData as xyz
2. make sure jsonUtility and jsonList are part of the project
3. (optionaly remove dbcon.py and drinkmixingmaschine.sql)





the drinkList jsonFile has the following json format:
{
"id":{
	"id" : integer
	unique identifier of the drink
	
	"name": string
	name of the drink
	
	"hopperid": integer or null
	if hopperid is an integer => drink is currently on the hopper
	if hopperid is null => drink is not currently on the hopper
	if mixdrink == true => hopperid should be null
	
	"dispensable" : boolean
	if true => drink can be dispensed
	if false => drink can't be dispensed
	all beverages on the hopper can be dispensed
	a mixdrink can be dispensed if all of their required drinks are on the hopper

	"flowspeed" : integer or null
	if the drink is a beverage => flowspeed = integer
	if the drink is a mixdrink => flowspeed = null	

	"mixdrink" : boolean
	if the drink requires muliple other drink it is considered a mixdrink

	"requiredDrinks" : [[drinkid :int, fillammount: int], ...]
	each element in "requiredDrinks" refers to the drinks that are required for it
	with their corresponding fillammounts.
	a drink that is not a mixdrink requires itself
	the fillammount for a non mixdrink is currently not used and therefore irrelevant
	if len(requiredDrinks) > 1  =>  mixdrink == False
},
	...
}
	
	
	