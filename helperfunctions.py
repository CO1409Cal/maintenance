import json
import os



class HelperFunctions:
    #Helper functions
    #------------------------------------------------------------#
    #Files

    @staticmethod
    def initialiseJSON(filename):
        if not os.path.exists(filename) or os.path.getsize(filename) == 0:
            with open(filename, "w") as f:
                json.dump([], f, indent=4)

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
        try:
            with open(filename,"r") as file: 
                # Python automatically closes the file after its out of scope
                data = file.read()
                data = HelperFunctions.toDict(data)
            return data 
        except FileNotFoundError as fe:
            if filename == "maintenance.json":
                with open(filename,"w") as file:
                    file.write("[")
            

           
    #JSON FILES
    #------------------------------------------------------------#
    @staticmethod
    def toJson(data,filename): #Provides better and valid formatting when writing to JSON files
        with open(filename, "r+") as file:
            HelperFunctions.initialiseJSON(filename)
            
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
            try:
                for task in machines:
                    if task["maintenanceId"] > nextid:
                        nextid = task["maintenanceId"]
            except TypeError:
                nextid = 1
                return nextid 
        else:
            print("Invalid filename provided. Please use 'machines.json' or 'maintenance.json'.")
            return None
        nextid += 1 #todo: Implement binary search
        return nextid

    @staticmethod
    def validateinput(type, input):
        match type:
            case "int":
                try: return int(input)
                except ValueError:
                    print("Invalid input. Please enter a valid integer.")
                    return None
            case "float":
                try: return float(input)
                except ValueError:
                    print("Invalid input. Please enter a valid float.")
                    return None
            case "str":
                try: return str(input)
                except ValueError:
                    print("Invalid input. Please enter a valid string.") 
                return None
            case "dict":
                try: return dict(input)
                except ValueError:
                    print("Invalid input. Please enter a valid dictionary.")
                    return None
            case _:
                print("Invalid type specified. Please use 'int', 'float', 'str', or 'dict'.")
                return None

    @staticmethod
    def checkForDuplicates(newObject):
        if hasattr(newObject, "model_dump"):
            comparisonObject = newObject.model_dump()
        else:
            comparisonObject = newObject

        comparisonObject.pop("maintenanceId", None)

        seenLog = "seenLog.json"
        if os.path.exists(seenLog):
            with open(seenLog,"r") as s:
                seen = set((json.load(s)))
        else:
            HelperFunctions.initialiseJSON(seenLog)
            seen = set()


        key = json.dumps(comparisonObject, sort_keys=True, default=str)

        if key in seen:
            return True
        else:
            seen.add(key)

        with open(seenLog, "w") as file:
            json.dump(list(seen), file, indent=4)
