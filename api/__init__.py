import json, urllib.request

class initialsettings:
    def __init__(self,appid,appkey,default_ATCO):
        self.appid = appid
        self.appkey = appkey
        self.default_ATCO = default_ATCO

def initialise():
    with open('apidata.json') as f:
        data=json.load(f)
    appid=data['appdata']['appid']
    appkey=data['appdata']['appkey']
    default_ATCO=data['default_settings']['default_ATCO']
    out=initialsettings(appid,appkey,default_ATCO)
    return out

progvars=initialise()

def getFromATCO(ATCO):
    global progvars
    with urllib.request.urlopen("https://transportapi.com/v3/uk/bus/stop/"+ATCO+"/live.json?app_id="+progvars.appid+"&app_key="+progvars.appkey+"&group=no&nextbuses=yes") as url:
        data = json.loads(url.read().decode())
    return(data)