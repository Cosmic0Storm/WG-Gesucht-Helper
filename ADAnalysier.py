from AD import AD 
from os import listdir
from subprocess import call
from OSMPythonTools.nominatim import Nominatim
import json
class ADAnalyser:
    
    cachednegativeAddresses=[" Nowackanlage 4 76137 Karlsruhe Südstadt"]
    forbiddenWords = ["Studentenverbindung","Verbindung","katholisch"]


    def __init__(self,filename):
        self.filename = filename
        with open(f"./data/{filename}","r",encoding="utf-8") as file:
            self.AD = AD(dict=json.loads(file.read()))

        
        

    def filterbyDefinition(self) -> bool: 
        for word in self.forbiddenWords:
            if word in self.AD.description:
                return False

        return True

    def geoLookupandFilterFraternity(self):
        self.nominatim = Nominatim()

        if self.AD.address[8:-2] not in self.cachednegativeAddresses:
            resultlist = self.nominatim.query(self.AD.address[8:-2])
            for result in resultlist.toJSON():
                
                if result["type"] == "fraternity":
                    self.cachednegativeAddresses.append(self.AD.address[8:-2])
                    return False

            return True
        else:
            return False

    def moveFileToNegativeFolder(self):
        call(["mv",f"./data/{self.filename}",f"./data/negative/{self.filename}"])

    def writeUrltoFile(self,adurl):
        with open("CandiateUrLs","a",encoding="utf-8") as urlfile:
            urlfile.write(f"{adurl}\n")

    def analyse(self):
        if not self.filterbyDefinition():
            self.moveFileToNegativeFolder()
            return
        if not self.geoLookupandFilterFraternity():
           self.moveFileToNegativeFolder()
           return
        self.writeUrltoFile(self.AD.url)
        

if __name__ == '__main__':
    files= listdir("./data")
    for file in files:
        if ".json" in file:
            newADAnalyser = ADAnalyser(file)
            newADAnalyser.analyse()




        

