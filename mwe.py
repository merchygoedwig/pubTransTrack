# The following is provided as a minimum working example of the api package provided in this project.

import api

busdata=api.getFromATCO(api.progvars.default_ATCO)
bus=api.busCreate(busdata)

for i in range(len(bus)):
    print(str(i+1)+': '+bus[i].line+' to '+bus[i].destination+' is due in '+str(divmod(bus[i].eta.seconds,60)[0])+' min(s)')

traindata=api.getFromTIPLOCCRS(api.progvars.default_)