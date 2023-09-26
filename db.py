import sqlite3

conn = sqlite3.connect('financeiro.sqlite')

cursor = conn.cursor()
SQL_QUERY = """ CREATE TABLE users (
    id integer PRIMARY KEY,
    nome text NOT NULL,
    ganhos float,
    despesas float
)"""
cursor.execute(SQL_QUERY)
