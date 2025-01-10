import sqlite3

DATABASE_NAME = "products.db"

def initiate_db():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            price INTEGER NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER NOT NULL,
            balance INTEGER NOT NULL DEFAULT 1000
        )
    ''')

    connection.commit()
    connection.close()

def get_all_products():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()

    connection.close()
    return products

def add_user(username, email, age):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute('''
        INSERT INTO Users (username, email, age, balance) 
        VALUES (?, ?, ?, ?)
    ''', (username, email, age, 1000))

    connection.commit()
    connection.close()

def is_included(username):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute('SELECT 1 FROM Users WHERE username = ?', (username,))
    user = cursor.fetchone()

    connection.close()
    return bool(user)
