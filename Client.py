import json
import socket


class Client:
    def __init__(self, ip, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((ip, port))

    def sender(self, text: str):
        self.client.send(text.encode('utf-8'))
        while self.client.recv(1024).decode('utf-8') != 'received':
            self.client.send(text.encode('utf-8'))

    def request_to_server(self, request: str):
        try:
            if request:
                self.sender(request)
                data = json.loads(self.client.recv(1024).decode('utf-8'))
                return data
        except Exception as e:
            print(f'Error: {str(e)}')
            exit(0)
