### MAIN ###
import signal
from SimpleWebServer1 import SimpleHTTPServer
import sys

def shutdownServer(sig, unused):
    """
    Shutsdown server from a SIGINT recieved signal
    """
    server.shutdown()
    sys.exit(1)

signal.signal(signal.SIGINT, shutdownServer)
server = SimpleHTTPServer(8085)
server.start()
print("Press Ctrl+C to shut down server.")
