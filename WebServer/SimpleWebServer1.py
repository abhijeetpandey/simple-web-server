import socket
import signal  # Allow socket destruction on Ctrl+C
import sys
import time
import threading


class SimpleHTTPServer(object):
    """
    Class for describing simple HTTP server objects
    """

    def __init__(self, port=8080, host='localhost'):
        self.host = host  # Default to any available network interface //change this one to local host
        self.port = port
        self.contentDir = 'web'  # Directory where webpage files are stored

    def start(self):
        """
        Attempts to create and bind a socket to launch the server
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            print("Starting server on {host}:{port}".format(host=self.host, port=self.port))
            self.socket.bind((self.host, self.port))
            print("Server started on port {port}.".format(port=self.port))

        except Exception as e:
            print("Error: Could not bind to port {port}".format(port=self.port))
            self.shutdown()
            sys.exit(1)

        self.listen()  # Start listening for connections

    def shutdown(self):
        """
        Shuts down the server
        """
        try:
            print("Shutting down server")
            self.socket.shutdown(socket.SHUT_RDWR)

        except Exception as e:
            pass  # Pass if socket is already closed

    def generate_headers(self, response_code):
        """
        Generate HTTP response headers.
        Parameters:
            - response_code: HTTP response code to add to the header. 200 and 404 supported
        Returns:
            A formatted HTTP header for the given response_code
        """
        header = ''
        if response_code == 200:
            header += 'HTTP/1.1 200 OK\n'
        elif response_code == 404:
            header += 'HTTP/1.1 404 Not Found\n'

        time_now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        header += 'Date: {now}\n'.format(now=time_now)
        header += 'Server: Simple-Python-Server\n'
        header += 'Connection: close\n\n'  # Signal that connection will be closed after completing the request
        return header

    def listen(self):
        """
        Listens on self.port for any incoming connections
        """
        self.socket.listen(5)
        while True:
            (client, address) = self.socket.accept()
            client.settimeout(60)
            print("Recieved connection from {addr}".format(addr=address))
            threading.Thread(target=self.handle_client, args=(client, address)).start()

    def handle_client(self, client, address):
        """
        Main loop for handling connecting clients and serving files from content_dir
        Parameters:
            - client: socket client from accept()
            - address: socket address from accept()
        """
        PACKET_SIZE = 1024
        while True:
            print("CLIENT", client)
            data = client.recv(PACKET_SIZE).decode()  # Recieve data packet from client and decode

            time.sleep(4)

            if not data: break

            request_method = data.split(' ')[0]
            print("Method: {m}".format(m=request_method))
            print("Request Body: {b}".format(b=data))

            if request_method == "GET" or request_method == "HEAD":
                # Ex) "GET /index.html" split on space
                file_requested = data.split(' ')[1]

                # If get has parameters ('?'), ignore them
                file_requested = file_requested.split('?')[0]

                if file_requested == "/":
                    file_requested = "/index.html"

                filepath_to_serve = self.contentDir + file_requested
                print("Serving web page [{fp}]".format(fp=filepath_to_serve))

                # Load and Serve files content
                try:
                    f = open(filepath_to_serve, 'rb')
                    if request_method == "GET":  # Read only for GET
                        response_data = f.read()
                    f.close()
                    response_header = self.generate_headers(200)

                except Exception as e:
                    print("File not found. Serving 404 page.")
                    response_header = self.generate_headers(404)

                    if request_method == "GET":  # Temporary 404 Response Page
                        response_data = b"<html><body><center><h1>Error 404: File not found</h1></center><p>Head back to <a href="">dry land</a>.</p></body></html>"

                response = response_header.encode()
                if request_method == "GET":
                    response += response_data

                client.send(response)
                client.close()
                break
            else:
                print("Unknown HTTP request method: {method}".format(method=request_method))
