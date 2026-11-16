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
   name: str
   online: bool
   uptime: float
   maintenanceAlerts: str
   maintenanceLog: dict[str,dict[str,datetime.datetime]]


class Maintenance(BaseModel):
    maintenanceId: int = 0 
    description: str = ""
    type: str = ""
    date: datetime.date
    downtime: int = 0
    priority: Priority = Priority.low
    cost: float  = 0.0



def create(Maintenance):
    maintenanceTask = Maintenance(
        maintenanceId = findNextID("machines.json"), #Automatically increment off last ID
        description = input(str("Enter description of maintenance : ")),
        date = datetime.datetime.strptime(input("Enter date of maintenance YYYY,MM,DD: "), "%Y,%m,%d").date(),
        downtime = input("Enter downtime in hours: "),
        priority = Priority(input("Priority: ")),
        cost = input("Enter the cost of the Maintenance: ")
    )
    downtime = maintenanceTask["downtime"]
    if downtime > 1 and downtime < 3 :
        maintenanceTask["type"] = "Routine"
    elif maintenanceTask["priority"] == "high" :
        maintenanceTask["type"] = "Urgent"
    else:
        maintenanceTask["type"] = "Preventative"

    return maintenanceTask


def automaticMaintenance(Maintenance):
    machineData = readFile("machines.json")
    dayInSeconds = (24*60) *60 #24 hours in seconds
    todaysDate = datetime.datetime(2026, 11, 16, 14, 55, 58) #16th november 2026 14 hours 55 minutes 58 zeconds


    for i in machineData:
        if machineData[i] == "Uptime:":
            if machineData[i+1] >= dayInSeconds or i["maintenanceAlerts"] != "":
                maintenanceTask = Maintenance(
                    maintenanceId = findNextID("machines.json"),
                    description = f"Automatic, {i["maintenanceAlerts"]}",
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
        file.write(json.dumps(data.model_dump(), default=str))

def readFile(filename):
    with open(filename,"r") as file:
        data = file.read()
        data = toDict(data)
    return data

def toDict(data):
    return json.loads(data)

def findNextID(filename):
    machines = readFile(filename)
    nextid = 0
    for machine in machines:
        for log in machine["maintenanceLog"].values():
            if log["id"] > nextid:
                nextid = log["id"] 
    return nextid + 1

#--------------------#






def main():
    while True:
        print(Maintenance)

if __name__ == "__main__":
    main()