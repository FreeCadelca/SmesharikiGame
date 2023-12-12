level_0 = {'node_pos': (110, 400), 'content': 'this is level 0', 'unlock': 1}
level_1 = {'node_pos': (300, 220), 'content': 'this is level 1', 'unlock': 2}
level_2 = {'node_pos': (480, 610), 'content': 'this is level 2', 'unlock': 3}
level_3 = {'node_pos': (610, 350), 'content': 'this is level 3', 'unlock': 4}
level_4 = {'node_pos': (880, 210), 'content': 'this is level 4', 'unlock': 5}
level_5 = {'node_pos': (1050, 400), 'content': 'this is level 5', 'unlock': 5}
# node_pos - узлы с координатами x,y
# unlock - номер уровня, который разблокируется
# всего 6 уровней, поэтому после прохождения 6-ого, мы остаёмся на 6-ом уровне
levels = {
    0: level_0,
    1: level_1,
    2: level_2,
    3: level_3,
    4: level_4,
    5: level_5}
# ^словарь уровней
