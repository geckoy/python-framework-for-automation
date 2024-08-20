from assetsserverProcess.general.BaseAssetsserver import BaseAssetsserver
from assetsserverProcess.general.assetsserverArgs import assetsserverArgs
from http.server import HTTPServer
from commands.serverHandler import server_Handler_Assets
from App.Helpers import env
from time import sleep
from socketserver import ThreadingMixIn

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
    pass

class assetsserver(BaseAssetsserver, assetsserverArgs):
    parallel = True
    parallelTimeout = 30
    def initilize(self) -> None:
        self.port = env("APP_ASSETS_PORT")
        self.address = env("APP_ASSETS_HOST")
        self.setProperties()
        self.SERVER : ThreadedHTTPServer = ThreadedHTTPServer((self.address,self.port), server_Handler_Assets())
        self.SERVER.timeout = 0.01

    def run(self):
        self.SERVER.handle_request()
        sleep(0.5)
                
    def app_close(self):
        pass