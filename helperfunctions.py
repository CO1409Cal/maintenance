import json
import os



class HelperFunctions:
    #Helper functions
    #------------------------------------------------------------#
    #Files
    @staticmethod    
    def writeToFile(data,filename,Isjson="yes"):
        if Isjson == "yes":
            HelperFunctions.toJson(data,filename) 

        if Isjson == "no":
            with open(filename,"a+") as file:

                jsondata = json.dumps(data, indent=4)
                file.write(jsondata)

    @staticmethod
    def toDict(data): 
            return json.loads(data)

    @staticmethod
    def readFile(filename): # Open and reads a file then returns a dict of the data
        with open(filename,"r") as file: 
            # Python automatically closes the file after its out of scope
            data = file.read()
            data = HelperFunctions.toDict(data)
        return data    
    #JSON FILES
    #------------------------------------------------------------#
    @staticmethod
    def toJson(data,filename): #Provides better and valid formatting when writing to JSON files
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
    #Misc
    @staticmethod
    def findNextID(filename):
        machines = HelperFunctions.readFile(filename) 
        nextid = 0

        if filename == "machines.json":
            for machine in machines:
                for log in machine["maintenanceLog"].values():
                    if log["id"] > nextid:
                        nextid = log["id"] 
        elif filename == "maintenance.json":
            for task in machines:
                if task["maintenanceId"] > nextid:
                    nextid = task["maintenanceId"]
        else:
            print("Invalid filename provided. Please use 'machines.json' or 'maintenance.json'.")
            return None
        nextid += 1 #todo: Implement binary search
        return nextid