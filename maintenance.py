from enum import Enum
from pydantic import BaseModel
from pydantic.dataclasses import dataclass
import datetime
import helperfunctions as h

h = h.HelperFunctions # Set alias for helper functions

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
            maintenanceId = h.findNextID("maintenance.json"), #Automatically increment off last ID
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
        machineData = h.readFile("machines.json")
        dayInSeconds = (24*60) *60 #24 hours in seconds
        todaysDate = datetime.datetime(2026, 11, 23, 9, 58, 32) #23rd november 2026 09 hours 58 minutes 32 zeconds


        for i in machineData:
            if i["uptime"] >= dayInSeconds or i["maintenanceAlerts"] != "":
                maintenanceTask = Maintenance(
                    maintenanceId = h.findNextID("maintenance.json"),
                    description = f"Automatic, {i["maintenanceAlerts"]}",
                    date = str(todaysDate.date()),
                    downtime = 1,
                    priority = Priority.medium,
                    cost = 10,
                )
                h.writeToFile(maintenanceTask.model_dump(), "maintenance.json")


    def modifyTask():
        taskID = int(input("Enter the maintenance ID of the task you want to modify: "))
        maintenanceData = h.readFile("maintenance.json")
        for i in maintenanceData:
            if i["maintenanceId"] == taskID:
                [description] = input("Enter new description (leave blank to keep current): ") or i["description"]
                [date] = input("Enter new date (YYYY-MM-DD) (leave blank to keep current): ") or i["date"]
                [downtime] = input("Enter new downtime in hours (leave blank to keep current): ") or i["downtime"]
                [priority] = input("Enter new priority (high, medium, low) (leave blank to keep current): ") or i["priority"]
                [cost] = input("Enter new cost (leave blank to keep current): ") or i["cost"]
                i["description"] = description
                i["date"] = date
                i["downtime"] = downtime
                i["priority"] = priority        
                i["cost"] = cost
                h.writeToFile(maintenanceData, "maintenance.json", Isjson="no")
                print(f"Task with ID {taskID} has been modified.")
                pass

    def deleteTask():
        taskID = int(input("Enter the maintenance ID of the task you want to delete: "))
        maintenanceData = h.readFile("maintenance.json")
        for i in maintenanceData:
            if i["maintenanceId"] == taskID:
                maintenanceData.remove(i)
                h.writeToFile(maintenanceData, "maintenance.json", Isjson="no") #calls helper function to write data to file
                print(f"Task with ID {taskID} has been deleted.")
                return
        print(f"No task found with ID {taskID}.")

    def displaytask():
        taskID = int(input("Enter the maintenance ID of the task you want to display: "))
        maintenanceData = h.readFile("maintenance.json")
        for i in maintenanceData:
            if i["maintenanceId"] == taskID:
                print(i["id"])
                print(i["description"])
                print(i["date"])
                print(i["downtime"])
                print(i["priority"])
                print(i["cost"])

#--------------------#

def main():
    while True:
        Maintenance.automaticMaintenance(Maintenance)
        h.writeToFile(Maintenance.create(Maintenance), "maintenance.json")
        Maintenance.displaytask()

if __name__ == "__main__":
    main()