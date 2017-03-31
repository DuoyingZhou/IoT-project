import urllib2,contextlib
from datetime import datetime
from collections import OrderedDict

from pytz import timezone
import gtfs_realtime_pb2
import google.protobuf

import vehicle,alert,tripupdate

class mtaUpdates(object):

    # Do not change Timezone
    TIMEZONE = timezone('America/New_York')
    
    # feed url depends on the routes to which you want updates
    # here we are using feed 1 , which has lines 1,2,3,4,5,6,S
    # While initializing we can read the API Key and add it to the url
    feedurl = 'http://datamine.mta.info/mta_esi.php?feed_id=1&key='
    apikey = '16358476092660b1ed5b98fb9204e871'
    VCS = {1:"INCOMING_AT", 2:"STOPPED_AT", 3:"IN_TRANSIT_TO"}    
    #tripUpdates = []
    #alerts = []

    def __init__(self):
        self.feedurl = self.feedurl + self.apikey

    # Method to get trip updates from mta real time feed
    def getTripUpdates(self):
        tripUpdates = []
        alerts = []
        feed = gtfs_realtime_pb2.FeedMessage()
        try:
            with contextlib.closing(urllib2.urlopen(self.feedurl)) as response:
                d = feed.ParseFromString(response.read())
        except (urllib2.URLError, google.protobuf.message.DecodeError) as e:
            print "Error while connecting to mta server " +str(e)
	

	timestamp = feed.header.timestamp
        nytime = datetime.fromtimestamp(timestamp,self.TIMEZONE)
	
	for entity in feed.entity:
	    # Trip update represents a change in timetable
	    if entity.trip_update and entity.trip_update.trip.trip_id:
		update = tripupdate.tripupdate()
#                print entity
                update.tripId =  entity.trip_update.trip.trip_id
                update.starttime = update.tripId[0:6]
                update.routeId = entity.trip_update.trip.route_id
                update.startDate = entity.trip_update.trip.start_date
                tripId = str(update.tripId)
                update.direction = tripId[-4]
                d_a_list = entity.trip_update.stop_time_update
                d_out=OrderedDict()
                for item in d_a_list:
                    
                    d_arrivetime=OrderedDict()
                    try:
                        d_arrivetime['arriveTime']=item.arrival.time
                    except:
                        continue
                    d_departtime = OrderedDict()
                    d_departtime['departTime'] = item.departure.time
                    d_out[str(item.stop_id)]=[d_arrivetime,d_departtime]
                    if str(item.stop_id)=='120S' or str(item.stop_id)=='120N':
                        update.timeto96 = item.arrival.time
                    if str(item.stop_id)=='127S' or str(item.stop_id)=='127N':
                        update.timeto42 = item.arrival.time
                    
                #print d_out         
                update.futureStops=d_out
                
                #print d_out 
                                
                #print  
		##### INSERT TRIPUPDATE CODE HERE ####	
                #self.tripUpdates.append(entity.trip_update)
	    if entity.vehicle and entity.vehicle.trip.trip_id:
	    	v = vehicle.vehicle()
                aaa = datetime.fromtimestamp(entity.vehicle.timestamp,self.TIMEZONE)
                v.timestamp = aaa.hour*60+aaa.minute
                v.dayofweek = aaa.weekday()+1
                v.currentStopStatus = entity.vehicle.current_status
                v.currentStopId = entity.vehicle.stop_id
		v.currentStopId = d_a_list[0].stop_id
                update.vehicleData = v
                tripUpdates.append(update)
                
	    if entity.alert:
                a = alert.alert()
               # print entity.alert
                try:
                    alist = entity.alert.header_text.translation
                   # print alist[0].text
                    a.alertMessage = alist[0].text
                    #a.tripId.append(update.tripId)
                    #a.routeId.append(update.routeId)
                    #a.startDate.append(update.startDate)
                    alerts.append(a)
                except:
                    #continue
                    #print "everything is awesome"
                    pass
        
                #### INSERT ALERT CODE HERE #####
#        print len(tripUpdates)
	return tripUpdates, alerts    
    # END OF getTripUpdates method
#m1=mtaUpdates()
#m1.getTripUpdates()
