import json
import os



class HelperFunctions:
    #Helper functions
    def writeToFile(data,filename,Isjson="yes"):
        if Isjson == "yes":
            ToJson(data,filename) # type: ignore

        if Isjson == "no":
            with open(filename,"a+") as file:

                jsondata = json.dumps(data, indent=4)
                file.write(jsondata)


    def readFile(filename):
        with open(filename,"r") as file:
            data = file.read()
            data = toDict(data) # type: ignore
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
        machines = readFile(filename) # type: ignore
        nextid = 0
        for machine in machines:
            for log in machine["maintenanceLog"].values():
                if log["id"] > nextid:
                    nextid = log["id"] 
        nextid += 1 #todo: Implement binary search
        return nextid