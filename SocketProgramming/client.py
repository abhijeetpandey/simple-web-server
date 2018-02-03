# Import socket module
import socket
import time

# Create a socket object

# Define the port on which you want to connect
port = 12345

# connect to the server on local computer
while True:
    s = socket.socket()
    s.connect(('127.0.0.1', port))

    # receive data from the server
    print s.recv(1024)
    # close the connection
    s.close()
    time.sleep(2)