from enum import Enum
from pydantic import BaseModel
from pydantic.dataclasses import dataclass
import datetime
import json
import os

class Priority(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"


class Maintenance(BaseModel):
    maintenanceId: int = 0 
    description: str = ""
    type: str = ""
    date: str
    downtime: int = 0
    priority: Priority = Priority.low
    cost: float  = 0.0


def create(Maintenance):
    maintenanceTask = Maintenance(
        maintenanceId = findNextID("machines.json"), #Automatically increment off last ID
        description = input(str("Enter description of maintenance : ")),
        date = str(datetime.datetime.strptime(input("Enter date of maintenance YYYY,MM,DD: "), "%Y,%m,%d").date()),
        downtime = input("Enter downtime in hours: "),
        priority = Priority(input("Priority: ")),
        cost = input("Enter the cost of the Maintenance: ")
    )
    maintenanceData = maintenanceTask.model_dump()
    downtime = maintenanceData["downtime"]
    if downtime > 1 and downtime < 3 :
        maintenanceData["type"] = "Routine"
    elif maintenanceData["priority"] == "high" :
        maintenanceData["type"] = "Urgent"
    else:
        maintenanceData["type"] = "Preventative"
    print("Maintenance Task Created: ")

    return maintenanceData


def automaticMaintenance(Maintenance):
    machineData = readFile("machines.json")
    dayInSeconds = (24*60) *60 #24 hours in seconds
    todaysDate = datetime.datetime(2026, 11, 23, 9, 58, 32) #23rd november 2026 09 hours 58 minutes 32 zeconds


    for i in machineData:
        if i["uptime"] >= dayInSeconds or i["maintenanceAlerts"] != "":
            maintenanceTask = Maintenance(
                maintenanceId = findNextID("machines.json"),
                description = f"Automatic, {i["maintenanceAlerts"]}",
                date = str(todaysDate.date()),
                downtime = 1,
                priority = Priority.medium,
                cost = 10,
            )
            writeToFile(maintenanceTask.model_dump(), "maintenance.json")


def modifyTask():
    taskID = int(input("Enter the maintenance ID of the task you want to modify: "))
    maintenanceData = readFile("maintenance.json")
    for i in maintenanceData:
        if i["maintenanceId"] == taskID:
            
            pass

def deleteTask():
    taskID = int(input("Enter the maintenance ID of the task you want to delete: "))
    maintenanceData = readFile("maintenance.json")
    for i in maintenanceData:
        if i["maintenanceId"] == taskID:
            maintenanceData.remove(i)
            writeToFile(maintenanceData, "maintenance.json", Isjson="no")
            print(f"Task with ID {taskID} has been deleted.")
            return
    print(f"No task found with ID {taskID}.")

#-------------------------------------------------------------------------#
#Helper functions
def writeToFile(data,filename,Isjson="yes"):
    if Isjson == "yes":
        ToJson(data,filename)

    if Isjson == "no":
        with open(filename,"a+") as file:

            jsondata = json.dumps(data, indent=4)
            file.write(jsondata)


def readFile(filename):
    with open(filename,"r") as file:
        data = file.read()
        data = toDict(data)
    return data

def toDict(data):
    return json.loads(data)

def ToJson(data,filename):
    with open(filename, "r+") as file:
        if not os.path.exists(filename) or os.path.getsize(filename) == 0:
            with open(filename, "w") as file:
                file.write("[\n")
                json.dump(data, file, indent=4)
                file.write("\n]")
            return
        
        with open(filename, "r+") as file:
            lines = file.read().strip()
            
            if lines.endswith("]"):
                file.seek(0, os.SEEK_END)
                file.seek(file.tell() - 1)
                file.truncate()    
    
                if lines != "[]":
                    file.seek(0, os.SEEK_END)
                    file.seek(file.tell() - 2)
                    file.write(",\n")
            file.write(json.dumps(data, indent=4))
            file.write("\n]")
            

        


def findNextID(filename):
    machines = readFile(filename)
    nextid = 0
    for machine in machines:
        for log in machine["maintenanceLog"].values():
            if log["id"] > nextid:
                nextid = log["id"] 
    nextid += 1 #todo: Implement binary search
    return nextid
    

#--------------------#






def main():
    while True:
        automaticMaintenance(Maintenance)
        writeToFile(create(Maintenance), "maintenance.json")
        print(Maintenance)

if __name__ == "__main__":
    main()