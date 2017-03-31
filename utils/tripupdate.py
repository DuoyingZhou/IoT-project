from collections import OrderedDict
# Storing trip related data
# Note : some trips wont have vehicle data
class tripupdate(object):
	def __init__(self):
	    self.tripId = None
            self.timeto96 = None
            self.timeto42 = None            
            self.starttime = None
	    self.routeId = None
	    self.startDate = None
	    self.direction = None
	    self.vehicleData = None
	    self.futureStops = OrderedDict() # Format {stopId : [arrivalTime,departureTime]}





