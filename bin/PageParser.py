#!/usr/bin/env python3


from bs4 import BeautifulSoup


class PageParser:
    def __init__(self, url, html):
        self.links = []
        self.url = url
        self.html = html

    def doSoup(self):
        self.soup = BeautifulSoup(self.html,'html.parser')
    
    def parseLinksOnPage(self):
        for a in self.soup.find_all("a"):
            if a.get('href'):
                self.links.append(a.get('href').strip())
        return self.links

    def parseImagesOnPage(self, baseUrl):
        for img in self.soup.find_all("img"):
            linkImage = ""
            if img.get('src'):
                linkImage = img.get('src').strip()
            if img.get('srcset'):
                for ss in img.get('srcset').split(" "):
                    if baseUrl in ss:
                        self.links.append(ss)
            if not linkImage and img.get('data-src'):
                linkImage = img.get('data-src').strip()
            if linkImage:
                self.links.append(linkImage)
        return self.links

    def parseAssets(self):
        for a in self.soup.find_all("link"):
            if a.get('href'):
                self.links.append(a.get('href').strip())
        for a in self.soup.find_all("script"):
            if a.get('src'):
                self.links.append(a.get('src').strip())
        return self.links

    def getAllUrlsOnPage(self, baseUrl):
        allLinks = self.parseLinksOnPage()
        allLinks.extend(self.parseImagesOnPage(baseUrl))
        allLinks.extend(self.parseAssets())
        return allLinks
