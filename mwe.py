# The following is provided as a minimum working example of the api package provided in this project.

import api

busdata=api.getFromATCO(api.progvars.default_ATCO)
bus=api.busCreate(busdata)

for i in range(len(bus)):
    print(str(i+1)+': '+bus[i].line+' to '+bus[i].destination+' is due in '+str(divmod(bus[i].eta.seconds,60)[0])+' min(s)')

print('\n')

traindata=api.getFromTIPLOCCRS(api.progvars.default_TIPLOCCRS)
train=api.trainCreate(traindata)

for i in range(len(train)):
    print(str(i+1)+': '+train[i].arrival.strftime("%H:%M ")+train[i].operator+' service to '+train[i].destination+' is due in '+str(train[i].eta)+' min(s). This service is currently '+train[i].status)