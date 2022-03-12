#!/usr/bin/python3
from ics import Calendar
import requests
import datetime
import sys

def getCal(url):

    cal = Calendar(requests.get(url).text)

    sorted_cal = sorted(cal.events)

    return sorted_cal

# cal is sorted by date. start < end
def getTimeframe(start, end, cal):
    
    for i in range(0,len(cal)):
        if(cal[i].begin.datetime.timestamp() > start.timestamp()): 
            startInd = i
            break
    for i in range(0,len(cal)):
        if(cal[i].end.datetime.timestamp() > end.timestamp()): 
            endInd = i
            break
    res_cal = cal[startInd:endInd]
    return res_cal
        

def getInput():
    # startString = input("Start date (yyyy mm dd): ")
    # year,month,day = startString.split(" ")
    # start = datetime.datetime(int(year),int(month),int(day))

    # endString = input("End date (yyyy mm dd): ")
    # year,month,day = endString.split(" ")
    # end = datetime.datetime(int(year),int(month),int(day))

    # if(end < start):
    #     print("Invalid Date")
    #     quit()

    args = sys.argv

    startString = args[1]
    endString = args[2]

    year,month,day = startString.split(".")

    start = datetime.datetime(int(year),int(month),int(day))

    year,month,day = endString.split(".")

    end = datetime.datetime(int(year),int(month),int(day))
    
    return start,end
    

def calculateHours(cal):
    minutes = 0
    i = 0
    while(i < len(cal)-1):
        event = cal[i]

        end = cal[i].end.datetime.timestamp()
        start = cal[i+1].begin.datetime.timestamp()

        loop = end > start

        # overlapping events
        if(cal[i].end.datetime.timestamp() > cal[i+1].begin.datetime.timestamp()):
            start = cal[i].begin.datetime
            # iterate until events are not overlapping anymore
            for j in range(i,len(cal)-1):
                if(cal[j].end.datetime.timestamp() <= cal[j+1].begin.datetime.timestamp()):
                    end = cal[j].end.datetime
                    i = j
                    break
            minutes += (end-start).total_seconds()/60
        # no overlap
        else:
            minutes += cal[i].duration.seconds/60
        i += 1
    minutes += cal[-1].duration.seconds/60
    return minutes/60


            
        

url = "https://calendar.google.com/calendar/ical/e3ddi1frfdpqhvbe5lrg4m03r0%40group.calendar.google.com/private-c42275d2cd5a124d401e007ab4594735/basic.ics"

start,end = getInput()

cal = getCal(url)

cal = getTimeframe(start, end, cal)

hours = calculateHours(cal)

print("The total hours in the specified Timeframe are " + str(hours))