import re

class Ingester:
    def __init__(self, config):
        self.config = config
        self.ignores = config.getConfig()['ingester']['ignore']
        self.hostPattern = re.compile("^"+config.configYaml['target']['base_url'])

    def validateUrl(self, link):
        for i in self.ignores:
            #print(re.search(i, link))<re.Match object; span=(0, 4), match='http'>
            if re.search(i, link):
                return False
        if re.match(self.hostPattern, link):
            return True    
        if link:            
            if link[0:2] == "//": ## amp dns-prefecth fix
                return False
            if link[0] == '/':
                return True
        
        return False
