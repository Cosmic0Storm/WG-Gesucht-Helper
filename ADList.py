import requests
import re
from bs4 import BeautifulSoup as bs4
import time
import AD

class ADList:

    def __init__(self,url):
        self.url = url 
        self.currenturl = url.format(number="0")
        self.domain = self.url.split("/")[2]
        self.adurls = []
        self.pageNumber = 0
        self.highestPageNumber = 0

        self.parser = AD.ADParser()

    def updateUrl(self):
        self.currenturl = self.url.format(number=str(self.pageNumber))

    def getPartofList(self):
        response = requests.get(self.currenturl)
        print(response.url)
        if response.status_code not in [200,300]:
            return
        else:
            return response.content.decode("utf-8")

    def writeUrltoFile(self,adurl):
        with open("urls","a",encoding="utf-8") as urlfile:
            urlfile.write(f"{adurl}\n")

    def parseAndBuildAdUrls(self,page):
        soup = bs4(page)
        ads = soup.select("div.wgg_card.offer_list_item")
        if len(ads)==0:
            return False
        if "asset_id" in ads[0].select_one("a")["href"]:
                return False
        for ad in ads:
            if "asset_id" in ad.select_one("a")["href"]:
                continue
            adurl = f"https://{self.domain}{ad.select_one('a')['href']}"
            self.adurls.append(adurl)
            self.writeUrltoFile(adurl)
        return True

    
            

    def generateADList(self):
        i = 0
        while (page := self.getPartofList()) is not None and (self.parseAndBuildAdUrls(page)):
            self.pageNumber += 1
            print(self.pageNumber)
            self.updateUrl()
            print(self.currenturl)
            time.sleep(15)
            if i % 3 == 0:
                time.sleep(60*5)
            i+=1

    def processADs(self):
        i = 0
        for adurl in self.adurls:
            self.parser.processAd(adurl)
            if i % 3:
                time.sleep(60*5)
            else:
                time.sleep(15)
            i += 1



if __name__ == '__main__':
    #Ads = ADList("https://www.wg-gesucht.de/wg-zimmer-und-1-zimmer-wohnungen-in-Karlsruhe.68.0+1.1.{number}.html")
    #Ads.generateADList()
    #time.sleep(60*10)
    #Ads.processADs()
    Parser = AD.ADParser()
    lines = []
    with open("urls","r",encoding="utf-8") as urlfile:
        lines = urlfile.readlines()
    i = 0
    for line in lines:
        Parser.processAd(line.replace("\n",""))
        if i % 3:
                time.sleep(60*5)
        else:
                time.sleep(15)
        i += 1
        
