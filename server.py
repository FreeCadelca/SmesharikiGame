from socket import *

server = socket(
    AF_INET, SOCK_STREAM
)
server.bind(
    ('127.0.0.1', 5000)
)

server.listen(2)

user, address = server.accept()
print(f'Connected:\n{user}\n{address}\n')


