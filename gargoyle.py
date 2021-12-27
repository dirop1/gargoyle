#!/usr/bin/env python3

import argparse
import textwrap
from bin.Petrifyer import Petrifyer
from bin.ConfigParser import ConfigParser
from bs4 import BeautifulSoup
from bin.OutPutDirectoryServer import OutputHttpServer
import time
import datetime
import sys
from bin.Outputter import Outputter


def start(config):
    petrifyer = Petrifyer(config)
    petrifyer.walkPages()

def copystatics(config):
    petrifyer = Petrifyer(config)
    petrifyer.copyOtherFiles()

def serve(config):
    print("Serving Current Folder...")
    server = OutputHttpServer(config)
    server.start_httpd()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='gargoyle',formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
         Please do not mess up this text!
         --------------------------------
             I have indented it
             exactly the way
             I want it
         '''),
        epilog='Enjoy the program! :)')
    parser.add_argument('action',
        metavar='action',
        type=str,
        help='Specify if you want to petrify or serve')
    parser.add_argument('path',
        metavar='path', default=".",
        type=str,
        help='Location of the gargoyle folder and where the site will be outputted to or server from')
    parser.add_argument('-s','--serve', help='Serve after petriffying')
    args = vars(parser.parse_args())
    print("Loading configuration")
    config = ConfigParser(args["path"]) 
    if args['action'] == "petrify":
        print("Petrifying")
        start(config);
    if args['action'] == "serve":
        print("Serving")
        serve(config);
    if args['action'] == "copystatic":
        copystatics(config);


    print(args)
    #print(args.petrify)
    # start()
