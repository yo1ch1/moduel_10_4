import threading
import time
import random
from queue import Queue

class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None

    def is_free(self):
        return self.guest is None

class Guest(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        time_to_wait = random.randint(3, 10)
        time.sleep(time_to_wait)

class Cafe:
    def __init__(self, *tables):
        self.queue = Queue()
        self.tables = list(tables)

    def guest_arrival(self, *guests):
        for guest in guests:
            is_table_free = False
            for table in self.tables:
                if not table.is_free():
                    continue
                table.guest = guest
                print(f'Гость {guest.name} сел за столик {table.number}')
                is_table_free = True
                break
            if not is_table_free:
                self.queue.put(guest)
                print(f'Гость {guest.name} встал в очередь')

    def discuss_guests(self):
        while not self.queue.empty() or self.tables:
            for table in self.tables:
                if table.guest and table.guest.is_alive():
                    print(f'{table.guest.name} покушал(-а) и ушел(ушла)')
                    print(f'Стол {table.number} свободен')
                    self.tables[self.tables.index(table)].guest = None
            for table in self.tables:
                if table.guest is None and self.queue.empty():
                    continue
                guest = self.queue.get()
                table.guest = guest
                print(f'{table.guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}')
                table.guest.start()

# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = [
'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()





