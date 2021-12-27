#!/usr/bin/env python3
import os
import yaml
import sys

class ConfigParser:
    def __init__(self, working_dir = os.getcwd()):
        if working_dir == ".":
            working_dir = os.getcwd()
        print("Loading configuration...")
        # Get the current working directory
        # print("Current working directory: {0}".format(working_dir))
        self.workingDir = working_dir
        sep = os.path.sep
        # print ("Checking config folder:" + str(os.path.exists('myDirectory')))
        configFile = working_dir + sep + 'gargoyle' + sep + 'config.yaml'
        if not os.path.exists(configFile):
            sys.exit("Could not get a gargoyle config file, run from the output gargoyle folder or pass the folder path as a program argument! Or pass -h to get help.")

        with open(configFile, 'r') as file:
            self.configYaml = yaml.load(file, Loader=yaml.FullLoader)
        self.startUrl = self.configYaml['target']['base_url'] + self.configYaml['target']['start_page']
        self.outputDir = os.path.join(os.path.normpath(self.workingDir), self.configYaml['outputter']['path'])
        print("Start page is " + self.startUrl )
    
    def getConfig(self):
        return self.configYaml
