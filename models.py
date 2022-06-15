import sqlite3
from typing import List


DATA = [
    {'id': 1, 'floor': 2, 'guestsnum': 3,'beds':2,'price':12,'chek_in':'2021-03-19','chek_out':'2021-03-21','firstname':'george','lastname':'sfa'},
    {'id': 2, 'floor': 1, 'guestsnum': 4,'beds':1,'price':13,'chek_in': '2021-03-22', 'chek_out': '2021-03-23','firstname':'george','lastname':'sfa'},
    {'id': 3, 'floor': 10, 'guestsnum': 6, 'beds': 4, 'price': 14,'chek_in': '2021-03-08', 'chek_out': '2021-03-24','firstname':'george','lastname':'sfa'},
    {'id': 4, 'floor': 10, 'guestsnum': 3, 'beds': 4, 'price': 14, 'chek_in': '20210308', 'chek_out': '20210311','firstname':'george','lastname':'sfa'},
]


class room:

    def __init__(self, id: int, floor: int,guestsnum:int, beds: int, price:int):
        self.id = id
        self.floor = floor
        self.guestsnum = guestsnum
        self.beds=beds
        self.price = price

    def __getitem__(self, item):
        return getattr(self, item)
class book:

    def __init__(self, id: int, chek_in: str, chek_out: str, room_id:int):
        self.id = id
        self.chek_in=chek_in
        self.chek_out=chek_out
        self.room_id=room_id

    def __getitem__(self, item):
        return getattr(self, item)


def init_db(initial_records: List[dict]):
    with sqlite3.connect('room.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name='room';"
        )
        exists = cursor.fetchone()
        # now in `exist` we have tuple with table name if table really exists in DB
        if not exists:
            cursor.executescript(
                'CREATE TABLE `room`'
                '(id INTEGER PRIMARY KEY AUTOINCREMENT, floor INTEGER ,guestsnum INTEGER ,beds INTEGER ,price INTEGER  )'
            )
            cursor.executemany(
                'INSERT INTO `room` '
                '(floor, guestsnum,beds,price) VALUES (?, ?,?,?)',
                [(item['floor'], item['guestsnum'],item['beds'],item['price']) for item in initial_records]
            )
            cursor.executescript(
                'CREATE TABLE `book`'
                '(id INTEGER PRIMARY KEY AUTOINCREMENT,firstname VARCHAR(100),lastname VARCHAR(100), chek_in VARCHAR(100) NOT NULL, chek_out VARCHAR(100) NOT NULL, '
                'room_id INTEGER NOT NULL,FOREIGN KEY (room_id) REFERENCES `room` (id) )'
            )
            cursor.executemany(
                'INSERT INTO `book` '
                '(firstname,lastname,chek_in,chek_out,room_id) VALUES (?, ?,?,?,?)',
                [(item['firstname'],item['lastname'],item['chek_in'], item['chek_out'], item['id']) for item in initial_records]
            )
def get_all_books(chek_in,chek_out,guestnum) -> List[room]:
    with sqlite3.connect('room.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT room.id,floor,guestsnum,beds,price from `room`, book WHERE book.chek_in=? and book.chek_out=? and book.room_id=room.id and room.guestsnum=?',(chek_in,chek_out,guestnum,))
        all_room = cursor.fetchall()
        return [room(*row) for row in all_room]

def add_books(floor,guestsnum,beds,price) -> str:
    with sqlite3.connect('room.db') as conn:
        cursor = conn.cursor()
        #try:
        cursor.execute('INSERT INTO room (floor,guestsnum,beds,price) VALUES (?,?,?,?)',(floor,guestsnum,beds,price,))
        return 'ok'
        #except BaseException:
            #return "mistake"

def add_bookings(firstname,lastname,chek_in,chek_out,room_id) -> str:
    with sqlite3.connect('room.db') as conn:
        cursor = conn.cursor()
        #try:
        cursor.execute('SELECT * FROM book WHERE firstname=? and lastname=? and chek_in=? and chek_out=? and room_id=?',(firstname,lastname,chek_in,chek_out,room_id,))
        result=cursor.fetchone()
        if result:
            return 'already'
        else:
            cursor.execute('INSERT INTO book (firstname,lastname,chek_in,chek_out,room_id) VALUES (?,?,?,?,?)',(firstname,lastname,chek_in,chek_out,room_id,))
            return 'ok'