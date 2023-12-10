import sys

for i in sys.stdin.readlines():
    i = i.split()
    print(f'\'{i[1]}\': \'{i[0]}\',')