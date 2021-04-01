import csv
from datetime import date
from glob import glob
import sys

year = date.today().year
mps=0
percentage=1

def getData(year, headingsWanted):
    globPattern = "Hughes "+str(year)+"*"
    files = glob(globPattern)
    if len(files) != 1:
        print("There must be exacly one file matching " + globPattern, file=sys.stderr)
        sys.exit(1)
    with open(files[0], newline='') as f:
        csvReader = csv.reader(f,delimiter=',', quotechar='"')
        members = {}
        n = 0
        for row in csvReader:
            if n == 0:
                
                fieldPositions = []
                width = len(row)
  #              print (row)
                i = 0
                for heading in row:
                    if heading in headingsWanted:
                        fieldPositions.append(i)
                    i += 1
                if len(fieldPositions) != len(headingsWanted):
                    print("Data for year " + str(year) + " has missing field", file=sys.stderr)
                    sys.exit(1)
            else:
                if width != len(row):
                    print ("Problem with width of line", n, line, file=sys.stderr)
                    sys.exit(1)
               
                record = []
                key = None
                for i in fieldPositions:
                    if key == None:
                        key = row[i]
                    else:
                        record.append(row[i])
   #             if n < 10:
   #                 print(key, record)
                members[key] = record
            n += 1
    return members

def floatAny(arg):
    try:
        value = float(arg)
        return value
    except ValueError:
        return 0
    
thisYear = getData(year,['National number', 'EBU rank', 'NGS grade','First name', 'Last name'])
lastYear = getData(year-1,['EBU number', 'EBU rank', 'NGS grade','First name', 'Last name'])
previousYear = getData(year-2,['EBU number', 'EBU rank', 'NGS grade','First name', 'Last name'])

qualifiers = []

    

for member in thisYear:
    if member in lastYear and floatAny(thisYear[member][percentage]) > floatAny(lastYear[member][percentage]) and floatAny(lastYear[member][percentage]) > 0:
        if floatAny(thisYear[member][percentage]) > 50 and  floatAny(lastYear[member][percentage]) <50:
            if member in previousYear and floatAny(previousYear[member][percentage]) <50:
                if lastYear[member][mps] in ["Local Master", "Club Master", "Area Master", "District Master", "CountyMaster", "Not public on ebu.co.uk"]:

                    improvement = round(floatAny(thisYear[member][percentage]) - floatAny(lastYear[member][percentage]),2)
                    person = thisYear[member]
                    name = person[2] + " " + person[3]
                    qualifiers.append(( member, name, previousYear[member][mps], person[mps] , previousYear[member][percentage], lastYear[member][percentage], person[percentage],
                                  improvement))
 
      
qualifiers.sort(key=lambda people: people[7], reverse=True)

with open('results.csv','w', newline='') as csvfile:
    w = csv.writer(csvfile)
    w.writerow(['EBU num', 'Name', 'Last year MPs', 'This year MPs', 'NGS 2 years ago', 'NGS 1 Year ago', 'NGS Now', 'Improvement'])
    for q in qualifiers:
        print (q)
        w.writerow(q)
 
 
