import requests
from bs4 import BeautifulSoup as bs4
import re
import json
class AD:

    def __init__(self,url="",page="",dict={}):
        if dict == {}:
            self.url = url
            self.page = page
            self.id = 0
            self.address = ""
            self.generalDetails = ""
            self.searchesfor = ""
            self.description = ""
            self.size = ""
            self.costs = ""
        else:
            self.url = dict["url"]
            self.id = dict["id"]
            self.address = dict["address"]
            self.generalDetails = dict["generalDetails"]
            self.searchesfor = dict["searchesfor"]
            self.description = dict["description"]
            self.size = dict["size"]
            self.costs = dict["costs"]

    def asdict(self):
        return {"url":self.url,"id":self.id,"address":self.address,"generalDetails":self.generalDetails,"searchesfor":self.searchesfor,"description":self.description,"size":self.size,"costs":self.costs}

    


class ADParser:

    def __init__(self):
        self.currentAd = None

    def processAd(self,url) -> bool:
        print(url)
        response = requests.get(url)
        if response.status_code not in [200,300]:
            print(f"AD failed to fetch trying again later")
            return 0
        else:
            newAD = AD(url=url,page=response.content.decode("UTF-8"))
            self.parsePageAndExtractrelevantInformation(newAD)
            self.writeToFiletoDisk(newAD)
            return 1 

    def parsePageAndExtractrelevantInformation(self,AD):
        soup = bs4(AD.page)
        if len(soup.select("div.alert.alert-with-icon.alert-warning")) == 1:
            return
        AD.id = re.sub(' +', ' ',soup.select_one("div.col-md-8.text-right").text)
        AD.address = re.sub(' +', ' ',soup.select_one("div.col-sm-4.mb10").text.replace("\n","")[7:-23])
        details = soup.select("div.col-sm-6")
        AD.generalDetails = re.sub(' +', ' ',details[0].text.replace("\n",""))
        AD.searchesfor = re.sub(' +', ' ',details[1].text.replace("\n",""))
        AD.description = re.sub(' +', ' ',soup.select_one("#ad_description_text").text.replace("\n",""))
        sizeandcosts= soup.select("div.col-xs-6.text-center.print_inline > h2.headline.headline-key-facts")
        AD.size = re.sub(' +', ' ',sizeandcosts[0].text.replace("\n","")).replace(" ","")
        AD.costs = re.sub(' +', ' ',sizeandcosts[1].text.replace("\n","")).replace(" ","")
        

    def writeToFiletoDisk(self,AD):
        jsonObj = json.dumps(AD.asdict(),indent=4)

        with open(f"./data/{AD.id}.json","w",encoding="utf-8") as outfile:
            outfile.write(jsonObj)


def new_func(Parser):
    print(Parser.parsedAds[0].url)
    print(Parser.parsedAds[0].id)
    print(repr(Parser.parsedAds[0].address))
    print(repr(Parser.parsedAds[0].generalDetails))
    print(repr(Parser.parsedAds[0].searchesfor))
    print(repr(Parser.parsedAds[0].description))
    print(repr(Parser.parsedAds[0].size))
    print(repr(Parser.parsedAds[0].costs))

if __name__ == "__main__":
    Parser = ADParser()
    Parser.processAd("https://www.wg-gesucht.de/wg-zimmer-in-Karlsruhe-Oststadt.8669928.html")
    Parser.writeToFiletoDisk()