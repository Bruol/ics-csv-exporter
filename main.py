#!/usr/bin/python3
from ics import Calendar
import requests
import datetime
import argparse

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

    msg = "Tool to analyze Google ical Calendar from url"

    parser = argparse.ArgumentParser(description = msg)

    parser.add_argument("-s","--start",help = "specify start Date wit the following format: YYYY.MM.DD")
    parser.add_argument("-e","--end",help = "specify end Date wit the following format: YYYY.MM.DD")
    parser.add_argument("-u","--url",help = "specify calendatr url")
    parser.add_argument("--csv",help = "export events to csv file with name hours-{start date}-{end date}.csv", action='store_true')
    parser.add_argument("--hours",help = "print total hours",action='store_true')


    args = parser.parse_args()

    csv = False
    hours = False

    if args.start:
        startString = args.start
    else:
        print("please specify start Date")
        quit()
    if args.end:
        endString = args.end
    else:
        print("please specify end Date")
        quit()
    if args.url:
        url = args.url
    else:
        print("please specify url")
        quit()

    year,month,day = startString.split(".")

    start = datetime.datetime(int(year),int(month),int(day))

    year,month,day = endString.split(".")

    end = datetime.datetime(int(year),int(month),int(day))
    
    return start,end,url,args.csv,args.hours   

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

def exportCsv(cal,filename):
    file = open(filename, 'w')
    date = "%d.%m.%Y"
    time = "%H:%M:%S"
    file.write("Titel, Datum, Startzeit, Endzeit, Dauer\n")
    for event in cal:
        file.write(f"{event.name},{event.begin.datetime.strftime(date)},{(event.begin.datetime + datetime.timedelta(hours=2)).strftime(time)},{(event.end.datetime + datetime.timedelta(hours=2)).strftime(time)},{int(event.duration.seconds/60)}\n")
    file.close()

        
def handleOverlaps(cal):
    i = 0
    while(i < len(cal)-1):
        if(cal[i].end.datetime.timestamp() > cal[i+1].begin.datetime.timestamp()):
            cal[i].end = cal[i+1].begin
        i += 1
    return cal

if __name__ == "__main__":
    start,end,url,csv,hours = getInput()

    cal = getCal(url)

    cal = getTimeframe(start, end, cal)

    if hours:
        total_hours = calculateHours(cal)
        print("The total hours in the specified Timeframe are " + str(total_hours))
    if csv:
        startString = start.strftime("%Y-%m-%d")
        endString = end.strftime("%Y-%m-%d")
        filename = f"hours-{startString}_{endString}.csv"
        cal = handleOverlaps(cal)
        exportCsv(cal, filename)
