import os
import re 


class Outputter:
    def __init__(self, config):
        self.config = config
        self.buildPaths(config)
        self.hostPattern = re.compile("^"+config.configYaml['target']['base_url'])
        self.overwrite = config.configYaml['outputter']['overwrite']
        self.endFilePattern = re.compile("^.*\..{1,5}$");

    def buildPaths(self, config):
        workingDir = config.workingDir
        outputPath = config.outputDir
        os.makedirs(outputPath, exist_ok = True)
        print("Outputtin to "+ outputPath)
        self.outputPath = outputPath

    def savePage(self, page):
        destPath = self.getHtmlPathOfLink(page.url)
        if not self.overwrite and os.path.exists(destPath):
            print(f" SaveSkipped!", end= "", flush= True)
            return
        os.makedirs(os.path.dirname(destPath), exist_ok = True)

        with open(destPath, "w", encoding="utf-8") as text_file:
            towrite = page.html #self.soup.prettify(formatter="minimal")
            if self.config.configYaml['target']['replace_host']:
                towrite = towrite.replace(self.config.configYaml['target']['base_url'], self.config.configYaml['target']['replace_host'])

            text_file.write( towrite )
    
    
    def cleanLink(self,link):
        return link.replace(self.hostFinal.split('//')[-1],self.hostName.split('//')[-1]).replace('https','http')

    def saveNonHtmlFile(self, req):
        path = self.getHtmlPathOfLink(req.getUrl())
        if not self.overwrite and os.path.exists(path):
            print(f" SaveSkipped!", end= "", flush= True)
            return
        os.makedirs(os.path.dirname(path), exist_ok = True)
        with open(path, 'wb') as f:
            f.write(req.getContent())

    def getHtmlPathOfLink(self,_link):
        parts = re.sub(self.hostPattern,"", _link).split('/')
        htmlPath = [self.outputPath]
        if not re.match(self.endFilePattern,parts[-1]): ## is a file
            if not parts[-1] or "/" not in parts[-1][-1]: # need to create index.html file
                parts.append("index.html")

        htmlPath.extend(parts)
        return os.path.join(self.outputPath,*htmlPath)


