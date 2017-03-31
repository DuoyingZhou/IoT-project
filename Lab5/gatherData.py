import time,csv,sys
from pytz import timezone
from datetime import datetime

sys.path.append('../utils')
import mtaUpdates1
import tripupdate,vehicle,alert,mtaUpdates1,aws

# This script should be run seperately before we start using the application
# Purpose of this script is to gather enough data to build a training model for Amazon machine learning
# Each time you run the script it gathers data from the feed and writes to a file
# You can specify how many iterations you want the code to run. Default is 50
# This program only collects data. Sometimes you get multiple entries for the same tripId. we can timestamp the 
# entry so that when we clean up data we use the latest entry

# Change DAY to the day given in the feed
DAY = datetime.today().strftime("%A")
TIMEZONE = timezone('America/New_York')

global ITERATIONS

#Default number of iterations
ITERATIONS = 500


#################################################################
####### Note you MAY add more datafields if you see fit #########
#################################################################

# column headers for the csv file
columns =['timestamp','tripId','route','day','timeToReachExpressStation','timeToReachDestination']


def main():
    # API key
    #with open('../../key.txt', 'rb') as keyfile:
    #    APIKEY = keyfile.read().rstrip('\n')
    #    keyfile.close()
    
	### INSERT YOUR CODE HERE ###
    data = []
    for i in range(0, ITERATIONS):
        updates = mtaUpdates1.mtaUpdates()
        tripupdates, alerts = updates.getTripUpdates()
        for i in range(0,len(tripupdates)):
            if str(tripupdates[i].routeId)=='1' or str(tripupdates[i].routeId)=='2' or str(tripupdates[i].routeId)=='3':
                if str(tripupdates[i].timeto96)!="None" and str(tripupdates[i].timeto42)!="None":
                    item = {}
                    item['index']     = str(time.time())
                    item['tripId']    = str(tripupdates[i].tripId)
                    item['timestamp'] = str(tripupdates[i].vehicleData.timestamp)
                    item['starttime'] = str(tripupdates[i].starttime)
                    if(str(tripupdates[i].routeId) == "1"):
                        item['route'] = "L"
                    else:
                        item['route'] = "E"
                    item['day']       = str(tripupdates[i].vehicleData.dayofweek)
                    item['timeto96']  = str(tripupdates[i].timeto96)
                    if item['timeto96'] == None:
                        continue
                    item['timeto42']  = str(tripupdates[i].timeto42)
                    if item['timeto42'] == None:
                        continue
                    data.append(item)
    file = open("P001.csv","a+")
    i = 1
    #file.write('index')
    #file.write('tripId')
    #file.write(','+'timestamp')
    #file.write(','+'starttime')
    #file.write(','+'route')
    #file.write(','+'day')
    #file.write(','+'timeto96')
    #file.write(','+'timeto42')
    for item in data:
        if i == 1:
            file.write('{0}'.format(item['index']))
        else:
            file.write('\n'+'{0}'.format(item['index']))
        file.write(','+'{0}'.format(item["tripId"]))
        file.write(','+'{0}'.format(item['timestamp']))
        file.write(','+'{0}'.format(item['starttime']))
        file.write(','+'{0}'.format(item['route']))
        file.write(','+'{0}'.format(item['day']))
        file.write(','+'{0}'.format(item['timeto96']))
        file.write(','+'{0}'.format(item['timeto42']))
        print i
        i = i + 1
    file.close()

main()               
                                    
