import json
import socket

"""
Represents a client.

Attributes:
    ip (str): The IP address of the client.
    port (int): The port of the IP address.

Methods:
    sender: sends an encoded message to a server.
    request_to_server: loads a message to string and sends to server and returns an answer from it
"""


class Client:
    def __init__(self, ip, port):
        """
        Initializes a new Client object.

        Args:
            ip (str): The IP address of the client.
            port (int): The port of the IP address.
        """
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((ip, port))

    def sender(self, text: str):
        """
        Sends a message to the server.

        Args:
            text (str): The text of the message to be sent to the server.
        """
        self.client.send(text.encode('utf-8'))
        while self.client.recv(1024).decode('utf-8') != 'received':
            self.client.send(text.encode('utf-8'))

    def request_to_server(self, request: str):
        """
        Sends a request to the server and receives the response.

        Args:
            request (str): The request to be sent to the server.

        Returns:
            data (dict): The data received from the server in response to the request.
        """
        try:
            if request:
                self.sender(request)
                data = json.loads(self.client.recv(1024).decode('utf-8'))
                return data
        except Exception as e:
            print(f'Error: {str(e)}')
            exit(0)
