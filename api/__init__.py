import json, urllib.request, math
from datetime import datetime

# A class to hold the default variables for the app: the App ID, App Key, the default ATCO and TIPLOC/CRS codes (both as failovers)
class initialsettings:
    def __init__(self,appid,appkey,default_ATCO,default_TIPLOCCRS):
        self.appid = appid
        self.appkey = appkey
        self.default_ATCO = default_ATCO
        self.default_TIPLOCCRS = default_TIPLOCCRS

# Function to initialise and set the default variables such that other functions defined here can use them
def initialise():
    with open('apidata.json') as f:
        data=json.load(f)
    appid=data['appdata']['appid']
    appkey=data['appdata']['appkey']
    default_ATCO=data['default_settings']['default_ATCO']
    default_TIPLOCCRS=data['default_settings']['default_TIPLOCCRS']
    out=initialsettings(appid,appkey,default_ATCO,default_TIPLOCCRS)
    return out

# Instantiation of an initialsettings class
global progvars
progvars=initialise()

# Function to make an GET request to the REST API asking for departures for a given ATCO Code, passing in App ID and Key using a the previously instantiated progvars (which is of the initialsettings class), which is declared global, this returns a nested Python dict
def getFromATCO(ATCO):
    if type(ATCO)!=str:
        ATCO=progvars.default_ATCO
    with urllib.request.urlopen("https://transportapi.com/v3/uk/bus/stop/"+ATCO+"/live.json?app_id="+progvars.appid+"&app_key="+progvars.appkey+"&group=no&nextbuses=yes") as url:
        data = json.loads(url.read().decode())
    return(data)

# Function to make an GET request to the REST API asking for departures for a given TIPLOC or CRS Code, passing in App ID and Key using a the previously instantiated progvars (which is of the initialsettings class), which is declared global, this returns a nested Python dict
def getFromTIPLOCCRS(TIPLOCCRS):
    if type(TIPLOCCRS)!=str:
        TIPLOCCRS=progvars.default_TIPLOCCRS
    trainurl=['https://transportapi.com/v3/uk/train/station/',TIPLOCCRS,'/live.json?app_id=',progvars.appid,'&app_key=',progvars.appkey,'&darwin=true&train_status=passenger']
    trainurl=''.join(trainurl)
    with urllib.request.urlopen(trainurl) as url:
        data = json.loads(url.read().decode())
    return(data)

# Creation of the bus class and a function to create a list of objects of class bus. Each bus holds five elements: line (a string of the bus route 'number'), destination (a string of the terminus of the bus), arrival (a datetime.datetime of the best estimate of arrival time), eta (a datetime.timedelta of the time between the arrival and the current time) and cancel (a bool showing if the bus has been cancelled).
class bus:
    def __init__(self,line,destination,arrival,eta,cancel):
        self.line = line
        self.destination = destination
        self.arrival = arrival
        self.eta = eta
        self.cancel = cancel

def busCreate(dict):
    buslist = []
    cflist = dict['departures']['all']
    num = len(cflist)
    now = datetime.now()
    try:
        for i in range(num):
            line = cflist[i]["line_name"]
            destination = cflist[i]["direction"]
            arrival = datetime.strptime(cflist[i]["date"]+cflist[i]["best_departure_estimate"],'%Y-%m-%d%H:%M')
            eta = arrival - now
            cancel = cflist[i]["status"]["cancellation"]["value"]
            buselem=bus(line,destination,arrival,eta,cancel)
            buslist.append(buselem)

    except NameError:
        for i in range(num):
            line = cflist[i]["line_name"]
            destination = cflist[i]["direction"]
            arrival = datetime.strptime(cflist[i]["date"]+cflist[i]["best_departure_estimate"],'%Y-%m-%d%H:%M')
            eta = arrival - now
            cancel = False
            buselem=bus(line,destination,arrival,eta,cancel)
            buslist.append(buselem)
    return buslist
#Class and function for holding timetable (scheduled) bus information. Each element on the busStop class is described in the documentation. The function is defined and takes in the values as seen, also accepting kwargs. The function can accept any kwarg, but the code checks for keys "time" and "date", if they are not provided, the variables of those names are set to an empty string (""). A HTTP GET is then performed with the defined args. The json file is loaded using json.loads and is dumped as a native Python dict. A list of class busStop is then created from the loaded json dump. Also included is the conversion of the date and time elements to a native Python datetime object under the "timestamp" element.
class busStop:
    def __init__(self,time,date,atcocode,name,stop_name,smscode,locality,
    bearing,indicator,latitude,longitude,timestamp):
        self.time = time
        self.date = date
        self.atcocode = atcocode
        self.name = name
        self.stop_name = stop_name
        self.smscode = smscode
        self.locality = locality
        self.bearing = bearing
        self.indicator = indicator
        self.latitude = latitude
        self.longitude = longitude
        self.timestamp = timestamp
    
def getLineFromArgs(operator,line,direction,atcocode=progvars.default_ATCO,**kwargs):
    checkdict = dict()
    
    for i in range(len(kwargs)):
        checkdict[list(kwargs.keys())[i]] = kwargs.get(list(kwargs.keys())[i])
    
    variables=["date","time"]
    #datetimeFormat=["%Y-%m-%d","%H:%M"]

    for i in range(len(variables)):
        if variables[i] not in checkdict:
            #checkdict[variables[i]] = datetime.strftime(datetime.now(),datetimeFormat[i])
            checkdict[variables[i]] = ""

    date = checkdict["date"]
    time = checkdict["time"]

    lineurl = ['https://transportapi.com/v3/uk/bus/route/',operator,'/',line,'/',direction,'/',atcocode,'/',date,'/',time,'/timetable.json?app_id=',progvars.appid,'&app_key=',progvars.appkey,'&edge_geometry=false&stops=all']
    lineurl=''.join(lineurl)
    
    with urllib.request.urlopen(lineurl) as url:
        data = json.loads(url.read().decode())
    
    busStopList = []
    stops=data['stops']

    for i in range(len(stops)):
        busStopList.append(busStop(stops[i]["time"], stops[i]["date"], stops[i]["atcocode"], stops[i]["name"], stops[i]["stop_name"], stops[i]["smscode"], stops[i]["locality"], stops[i]["bearing"], stops[i]["indicator"], stops[i]["latitude"], stops[i]["longitude"],
        datetime.strptime(stops[i]["date"]+stops[i]["time"],"%Y-%m-%d%H:%M")
        ))

    return busStopList

# Creation of the train class and a function to create a list of objects of class train. Each "train" holds seven elements: arrival (a datetime.datetime showing estimated arrival time); eta (an int showing estimated time of arrival in minutes); operator (a str holding the long name of the TOC); destination (a str showing the train's terminus station); origin (a str showing the train's origin station); status (a str showing the current status of the train, i.e. "ON TIME") and uid (a str showing the UID of the train imported from TRUST).
class train:
    def __init__(self,arrival,eta,operator,destination,origin,status,uid):
        self.arrival = arrival
        self.eta = eta
        self.operator = operator
        self.destination = destination
        self.origin = origin
        self.status = status
        self.uid = uid

def trainCreate(dict):
    trainlist = []
    timestamp=dict['request_time']
    date=timestamp.split('T')[0]
    cflist = dict['departures']['all']
    num = len(cflist)
    for i in range(num):
        arrival = datetime.strptime(date+cflist[i]['expected_departure_time'],'%Y-%m-%d%H:%M')
        eta = cflist[i]['best_departure_estimate_mins']
        operator = cflist[i]['operator_name']
        destination = cflist[i]['destination_name']
        origin = cflist[i]['origin_name']
        status = cflist[i]['status']
        uid = cflist[i]['train_uid']
        trainelem=train(arrival,eta,operator,destination,origin,status,uid)
        trainlist.append(trainelem)
    return trainlist