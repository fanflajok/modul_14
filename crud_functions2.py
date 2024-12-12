import sqlite3
import string

def initiate_db():
    connection = sqlite3.connect('initiate_db.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL)
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    balance NOT NULL)
    ''')
    connection.commit()
    connection.close()


def get_all_products():
    connection = sqlite3.connect('initiate_db.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()
    connection.commit()
    connection.close()
    return products

def add_user(username, email, age, balance=1000):
    connection = sqlite3.connect('initiate_db.db')
    cursor = connection.cursor()
    cursor.execute(f'''
INSERT INTO Users(username, email, age, balance) VALUES('{username}','{email}','{age}' , '{balance}')
    ''')
    connection.commit()
    connection.close()

def add_products(title,description, price):
    connection = sqlite3.connect('initiate_db.db')
    cursor = connection.cursor()
    cursor.execute(f'''
INSERT INTO Products(title, description, price) VALUES('{title}','{description}','{int(price)}')
    ''')
    connection.commit()
    connection.close()

def is_included(username):
    connection = sqlite3.connect('initiate_db.db')
    cursor = connection.cursor()
    check = cursor.execute('SELECT * FROM Users WHERE username=?', (username,))
    if check.fetchone() is None:
        return False
    else:
        return True


def isinstance_checked(messages_for_calc_or_registration):
    if isinstance(messages_for_calc_or_registration, int):
        return True
    else:
        return False

def checked_is_english(data_for_sql):
    return all(char.lower() in string.ascii_lowercase for char in data_for_sql)

def is_included_mail(email):
    connection = sqlite3.connect('initiate_db.db')
    cursor = connection.cursor()
    check = cursor.execute('SELECT * FROM Users WHERE email=?', (email,))
    if check.fetchone() is None:
        return False
    else:
        return True
initiate_db()