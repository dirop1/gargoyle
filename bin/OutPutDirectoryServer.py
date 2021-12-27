from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
from pathlib import Path
import sys

#http.server is not recommended for production. It only implements basic security checks.
class OutputHttpServer:
    def __init__(self, config):
        self.port = config.getConfig()['http_server']['port']
        self.directory = config.outputDir
        if not os.path.exists(config.outputDir):
            sys.exit("Not a valid output dir")

    def start_httpd(self):
        print(f"serving {self.directory} at http://localhost:{self.port}")
        handler = partial(SimpleHTTPRequestHandler, directory=self.directory)
        httpd = HTTPServer(('localhost', self.port), handler)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass

        httpd.server_close()
        print("Server stopped.")