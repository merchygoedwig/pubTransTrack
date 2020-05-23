import json, urllib.request, math
from datetime import datetime

# A class to hold the default variables for the app: the App ID, App Key and the default ATCO Code (a failover)
class initialsettings:
    def __init__(self,appid,appkey,default_ATCO):
        self.appid = appid
        self.appkey = appkey
        self.default_ATCO = default_ATCO

# Function to initialise and set the default variables such that other functions defined here can use them
def initialise():
    with open('apidata.json') as f:
        data=json.load(f)
    appid=data['appdata']['appid']
    appkey=data['appdata']['appkey']
    default_ATCO=data['default_settings']['default_ATCO']
    out=initialsettings(appid,appkey,default_ATCO)
    return out

# Instantiation of an initialsettings class
progvars=initialise()

# Function to make an GET request to the REST API asking for departures for a given ATCO Code, passing in App ID and Key using a the previously instantiated progvars (which is of the initialsettings class), which is declared global, this returns a nested Python dict
def getFromATCO(ATCO):
    global progvars
    with urllib.request.urlopen("https://transportapi.com/v3/uk/bus/stop/"+ATCO+"/live.json?app_id="+progvars.appid+"&app_key="+progvars.appkey+"&group=no&nextbuses=yes") as url:
        data = json.loads(url.read().decode())
    return(data)

# Creation of the bus class and a function to instantiate it and fill it with the required objects, the objects held in bus are: list (the slice of the dict returned previously accessed by somevar['departures']['all']); number (the number of elements in list); operator (a set of the list returned by iteration over the slice list[i]['operator name']) and simplist (a simplified version of list containing a dict with elements with keys "service", "destination", "date", "time", "estimated" and "cancel").
class bus:
    def __init__(self,list,number,operator,simplist):
        self.list=list
        self.number=number
        self.operator=operator
        self.simplist=simplist

def busCreate(dict):
    number=len(dict['departures']['all'])
    list=dict['departures']['all']
    operator=[]
    simplist = []
    for i in range(number):
        operator.append(list[i]['operator_name'])
        duetime=datetime.strptime(list[i]["date"]+list[i]["best_departure_estimate"],'%Y-%m-%d%H:%M')
        now=datetime.now()
        due=duetime-now
        due=math.ceil(due.seconds/60)
        try:
            simplist.append(
                {"service": list[i]["line_name"],
                "destination": list[i]["direction"],
                "date": list[i]["date"],
                "time": list[i]["best_departure_estimate"],
                "estimated": due,
                "cancel": list[i]["status"]["cancellation"]["value"]}
            )
        except NameError:
            simplist.append(
                {"service": list[i]["line_name"],
                "destination": list[i]["direction"],
                "date": list[i]["date"],
                "time": list[i]["best_departure_estimate"],
                "estimated": due,
                "cancel": False})
    operator=set(operator)

    out=bus(list,number,operator,simplist)
    return out
                