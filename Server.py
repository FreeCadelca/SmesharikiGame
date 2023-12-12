import json
import socket
import sqlite3


class Server:
    def __init__(self, ip: str, port: int, database_name: str = "DatabaseOfAccounts.sqlite3"):
        self.database_name = database_name
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((ip, port))
        print(f'Server Ip: {ip}\nServer port: {port}\n')
        self.server.listen(3)

    def sender(self, user: socket.socket, text: str):
        user.send(text.encode('utf-8'))

    def run(self):
        while True:
            user, address = self.server.accept()
            print(f'Client connected\n\tip: {address[0]}\n\tport: {address[1]}')
            self.listen(user)

    def listen(self, user: socket.socket):
        is_work = True
        while is_work:
            data = ''
            try:  # trying to get message from client
                data = user.recv(1024)
                self.sender(user, 'received')
            except Exception as e:
                is_work = False
            if len(data) > 0:
                data = json.loads(data.decode('utf-8'))
                print(f'The request has been got:\n\t{data}')
                msg = data['msg']
                cfg = json.loads(data['cfg'])
                if msg == "disconnect":
                    self.sender(user, 'You are disconnected')
                    user.close()
                    is_work = False
                else:  # if msg is a command
                    to_send = {'answer': '', 'error': ''}

                    if len(msg) > 8 and msg[:7] == 'SignIn ':
                        try:
                            request_data = msg.split(' ')
                            new_login = request_data[1]
                            new_hashed_password = request_data[2]

                            connection = sqlite3.connect(self.database_name)
                            cursor = connection.cursor()
                            cursor.execute("select * from Accounts where Login = ?", (new_login,))
                            result = cursor.fetchall()
                            if not len(result):  # if this login doesn't exist
                                cursor.execute(
                                    "insert into Accounts (Login, Hashed_password, Coins) values (?, ?, ?)",
                                    (new_login, new_hashed_password, 0,)
                                )
                                cfg["current_user"] = new_login
                                cfg["coins"] = 0
                                connection.commit()
                                cursor.close()
                                to_send['answer'] = 'successfully added new account'
                            else:
                                to_send['answer'] = 'failed sign in, login already exists'
                        except Exception as e:
                            to_send['error'] = str(e)
                    elif len(msg) > 5 and msg[:6] == 'LogIn ':
                        try:
                            request_data = msg.split(' ')
                            login = request_data[1]
                            hashed_password = request_data[2]

                            connection = sqlite3.connect(self.database_name)
                            cursor = connection.cursor()
                            cursor.execute(
                                "select * from Accounts where Login = ?",
                                (login,)
                            )
                            result = cursor.fetchall()
                            if len(result):  # if this login exist
                                row = result[0]
                                if row[1] == hashed_password:
                                    to_send['answer'] = 'successfully logged in the account'
                                    cfg["current_user"] = login
                                    cfg["coins"] = row[2]
                                else:
                                    to_send['answer'] = 'failed logged in, wrong password'
                            else:
                                to_send['answer'] = 'failed logged in, the account doesnt exist'
                        except Exception as e:
                            to_send['error'] = str(e)
                    elif msg == 'UpdateCoins':
                        if cfg["current_user"] != "guest":
                            connection = sqlite3.connect(self.database_name)
                            cursor = connection.cursor()
                            cursor.execute(
                                "update Accounts set Coins = ? where Login = ?",
                                (cfg["coins"], cfg["current_user"],)
                            )
                    else:
                        to_send['error'] = 'there is no such command'
                    to_send['cfg'] = cfg
                    self.sender(user, json.dumps(to_send))
                    print(f'The response has been sent:\n\t{to_send}')
            else:
                print("Client disconnected\n")
                is_work = False


s = Server('127.0.0.1', 4444)
s.run()
