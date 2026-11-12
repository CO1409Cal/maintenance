from pydantic import BaseModel
from pydantic.dataclasses import dataclass
import datetime
import json


class Machine(BaseModel):
   online: bool
   uptime: float
   name: str
   maintenanceAlerts: str
   maintenanceLog: dict[str,str,datetime.datetime]


class Maintenance(BaseModel):
     maintenanceId: int
     type: str
     date: datetime.date
     downtime: int
     priority: Priority 
     cost: float  
       
        #def __init__(self):
        #    self.maintenanceId = 0
        #    self.type = ""
        #    self.date = datetime.date
        #    self.downtime = 0
        #    self.priority = Priority
        #    self.cost = 0.0

class Priority:
    def __init__(self):
        self.high 
        self.medium
        self.low

def create(Maintenance):
    maintenanceTask = Maintenance(
        maintenanceId = 1, #Automatically increment off last ID
        type = input(str("Enter type of maintenance \n Preventative \n Routine \n Urgent \n : ")),
        date = input("Enter date of maintenance DD/MM/YYYY: "),
        downtime = input("Enter downtime in hours: "),
        priority = input("Priority: "),
        cost = input("Enter the cost of the Maintenance: ")
    )
    return maintenanceTask


def automaticMaintenance(Maintenance):
    readFile(machines.json)


def writeToFile(data,filename):
    with open(filename,"a") as file:
        file.write(json.dumps(data.dict(), default=str))

def readFile(filename):
    with open(filename,"r") as file:
        data = file.read(json.dump())
    return data


#def scheduleMaintenance(machineName):
#    global menuChoice
#    Machine.name = machineName
#    date = input("Enter the date for maintenance (YYYY-MM-DD): ")
#    maintainWorkload = input("Enter the estimated time the task will require (HHH-MM): ")
#
#    Machine.maintenanceLog = date + maintainWorkload

def main():
    while True:
        writeToFile(create(Maintenance), "maintenance.json")
        print(Maintenance)

if __name__ == "__main__":
    main()