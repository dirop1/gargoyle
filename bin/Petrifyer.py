#!/usr/bin/env python3
import os

from yaml import safe_load
from bin.Ingester import Ingester
from bin.Outputter import Outputter
from bin.PageParser import PageParser
from bin.ReqGetter import ReqGetter
import time

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Petrifyer:
    visitedLinks = []
    errors= []
    linksToVisit = []
    invalidLinks = []
    MAX_VISITS = 10000
    def __init__(self, config):
        print("Petrifyer Started")
        self.config = config
        self.linksToVisit.append(config.startUrl)
        self.ingester = Ingester(config)
        self.outputter = Outputter(config)
    
    def walkPages(self):
        req = ReqGetter()
        while len(self.linksToVisit) > 0 and len(self.visitedLinks) < self.MAX_VISITS:
            print(f"- {bcolors.OKBLUE}{len(self.visitedLinks)}/{len(self.linksToVisit)}{bcolors.ENDC} - {bcolors.WARNING} {self.linksToVisit[0]}{bcolors.ENDC}", end="", flush=True)
            req.get(self.linksToVisit[0])
            print(f" {bcolors.OKGREEN} {req.getContentType()} - {req.getStatusCode()} {bcolors.ENDC}", end="", flush=True);
            if req.getStatusCode() != 200:
                self.errors.append({ req.getStatusCode(), self.linksToVisit[0]})
                print(f"{bcolors.FAIL} http request failed {req.getStatusCode()} {bcolors.ENDC}")
                self.errors.append(req.getUrl())
                self.linksToVisit.remove(req.getUrl())
            else:
                if "text/html" in req.getContentType():
                    page = PageParser(url=req.getUrl(), html = req.getText())
                    page.doSoup()
                    try:
                        print(" parsing links", end="", flush=True)
                        newLinks = page.getAllUrlsOnPage(self.config.getConfig()['target']['base_url'])
                        print(f" found({len(newLinks)})", end="", flush=True)
                        added = 0
                        for nl in newLinks:
                            if "#" in nl:
                                nl = nl.split("#")[0]
                            if nl not in self.invalidLinks:
                                urlValid = self.ingester.validateUrl(nl)
                                if urlValid:
                                    if nl[0] == '/':
                                        nl = self.config.getConfig()['target']['base_url'] + nl
                                        dqf = nl.split("//") #doubleQuotesFix
                                        if len(dqf) > 2:
                                            nl = dqf[0] + "//" + dqf[1] + "/" + dqf[2]
                                    if not (nl in self.visitedLinks or nl in self.linksToVisit):
                                        self.linksToVisit.append(nl)
                                        added = added + 1
                                else:
                                    self.invalidLinks.append(nl)
                        print(f" added({added}) saving page", end="", flush=True)                             
                        self.outputter.savePage(page)
                        self.stepFowardUrl(page.url)
                    except Exception as err:
                        self.errors.append(req.getUrl())
                        print(f"{bcolors.FAIL} {err} {bcolors.ENDC}" + req.getUrl())
                        time.sleep(self.config.getConfig()['target']['delay'])
                else: # not text/html
                    #just save the file
                    self.outputter.saveNonHtmlFile(req)
                    self.stepFowardUrl(req.getUrl())



                print(f" {bcolors.OKGREEN}Done! {bcolors.ENDC} sizes->", len(self.visitedLinks), len(self.invalidLinks), len(self.errors))
                time.sleep(self.config.getConfig()['target']['delay'])
        print("Petrifyer ended")
        self.saveUrls(self.visitedLinks,"visitedLinks.txt")
    

    def stepFowardUrl(self, url):
        self.visitedLinks.append(url)
        try:
            self.linksToVisit.remove(url)
        except:
            try:
                if url[-1] != '/':
                    self.linksToVisit.remove(url + "/")
                else:
                    self.linksToVisit.remove(url[0:-1])
            except:
                pass


    def addOtherFiles(self):
        other_files = self.config.getConfig()['outputter']['other_files']
        for f in other_files:
            f = self.config.getConfig()['target']['base_url'] + f
            print("adding other_files " + f)
            self.linksToVisit(f)

    def saveUrls(self, urlArray,filename):
         with open(os.path.join(self.config.outputDir, filename), "w", encoding="utf-8") as text_file:
            towrite = ""
            for l in urlArray:
                towrite = towrite + l + "\n"
            text_file.write( towrite )






