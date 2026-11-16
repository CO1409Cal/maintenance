from enum import Enum
from pydantic import BaseModel
from pydantic.dataclasses import dataclass
import datetime
import json

class Priority(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"

class Machine(BaseModel):
   online: bool
   uptime: float
   name: str
   maintenanceAlerts: str
   maintenanceLog: dict[str,dict[str,datetime.datetime]]


class Maintenance(BaseModel):
    maintenanceId: int = 0
    type: str = ""
    date: datetime.date
    downtime: int = 0
    priority: Priority = Priority.low
    cost: float  = 0.0




def create(Maintenance):
    maintenanceTask = Maintenance(
        maintenanceId = 1, #Automatically increment off last ID
        type = input(str("Enter type of maintenance \n Preventative \n Routine \n Urgent \n : ")),
        date = datetime.datetime.strptime(input("Enter date of maintenance YYYY,MM,DD,HH: ")),
        downtime = input("Enter downtime in hours: "),
        priority = Priority.input("Priority: "),
        cost = input("Enter the cost of the Maintenance: ")
    )
    return maintenanceTask


def automaticMaintenance(Maintenance):
    machineData = readFile("machines.json")
    dayInSeconds = (24*60) *60 #24 hours in seconds
    todaysDate = datetime.datetime(2026, 11, 16, 14, 55, 58) #16th november 2026 14 hours 55 minutes 58 zeconds


    for i in machineData:
        if machineData[i] == "Uptime:":
            if machineData[i+1] >= dayInSeconds:
                maintenanceTask = Maintenance(
                    maintenanceId = 1,
                    type = "Automatic",
                    date = todaysDate,
                    downtime = 1,
                    priority = Priority.medium,
                    cost = 10,
                )
                return maintenanceTask

#-------------------------------------------------------------------------#
#Helper functions
def writeToFile(data,filename):
    with open(filename,"a") as file:
        file.write(json.dumps(data.dict(), default=str))

def readFile(filename):
    with open(filename,"r") as file:
        data = file.read()
        data = toDict(data)
    return data

def toDict(data):
    return json.loads(data)

def findlastID(filename):
    machines = readFile(filename)
    nextid = 0
    for i in machines:
        if machines[maintenanceLog][id] > nextid:
            nextid = machines[maintenanceLog][id] + 1
    return nextid

#--------------------#






def main():
    while True:
        writeToFile(create(Maintenance), "maintenance.json")
        print(Maintenance)

if __name__ == "__main__":
    main()