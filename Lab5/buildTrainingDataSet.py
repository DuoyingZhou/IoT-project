## This program is used to clean out the data from the csv that you collected.
## It aims at removing duplicate entries and extracting any further insights 
## that the author(s) of the code may see fit

## Usage (for file as is currently): python buildTrainingDataSet.py <filename of file from part 1>
  
import sys

# Pandas is a python library used for data analysis
import pandas
from pandas import read_csv
from pytz import timezone
from datetime import datetime


TIMEZONE = timezone('America/New_York')


def main(fileHandle):
	# This creates a dataframe
	rawData = read_csv(fileHandle)

	# Remove duplicate entries based on tripId, retain the one with maximum timestamp
	data = rawData.groupby('tripId').apply(lambda x: x.ix[x.timestamp.idxmax()])
        data = data.iloc[:,[0,2,3,4,5,6,7]]

	# Seperate all the local trains and form a new data frame
	localTrains = data[data.route == 'L']
        # print localTrains
	# Express trains
	expressTrains = data[data.route == 'E']
        #print expressTrains
	# 1. Find the time difference (to reach 96th) between all combinations of local trains and express
	# 2. Consider only positive delta
	# 3. Make the final table
        T = []
        #for l in localTrains:
        #    for e in expressTrains:
        #        gap = e.timeto96 - l.timeto96
        #        print gap
        print localTrains
        T = []
        for i in range(0, len(localTrains)):
            for j in range(0, len(expressTrains)):
                gap = expressTrains.iloc[j,5] - localTrains.iloc[i, 5]
                if gap > 0:
                    t = {}
                    t['TimeStamp'] = localTrains.iloc[i,1]
                    t['delta96']   = gap
                    t['delta42']   = expressTrains.iloc[j,6] - localTrains.iloc[i, 6]
                    t['Day']       = localTrains.iloc[i,4]
                    if t['delta42'] >= 0:
                        t['class'] = 'no'
                    else:
                        t['class'] = 'yes'
                    T.append(t)
        with open("Train.csv", 'w') as file:
          #  i = 0
            file.write('TimeStamp,delta96,delta42,Day,class'+'\n')
            for t in T:
                # if i == 0:
                #    file.write('{0}'.format(t['TimeStamp']))
                # else:
                file.write('{0}'.format(t['TimeStamp']))
                file.write(','+'{0}'.format(t['delta96']))
                file.write(','+'{0}'.format(t['delta42']))
                file.write(','+'{0}'.format(t['Day']))
                file.write(','+'{0}'.format(t['class'])+'\n')
                print i
                i = i + 1


	# Create a new data frame for final table
#	finalData = pandas.DataFrame()


	############## INSERT YOUR CODE HERE ###############
	
#	finalData.to_csv("finalData.csv",index=False)



if __name__ == "__main__":

	lengthArg = len(sys.argv)


	if lengthArg < 2:
		print "Missing arguments"
		sys.exit(-1)

	if lengthArg > 2:
		print "Extra arguments"
		sys.exit(-1)
	
	fileHandle = sys.argv[1]
	main(fileHandle)
