import requests

class ReqGetter:
    def __init__(self):
        pass

    def get(self,url):
        self.r = requests.get(url)
        # print(self.r.headers)

    def getText(self):
        return self.r.text
    def getUrl(self):
        return self.r.url
    def getStatusCode(self):
        return self.r.status_code

    def getContentType(self):
        return self.r.headers['Content-Type']
    
    def getContent(self):
        return self.r.content
