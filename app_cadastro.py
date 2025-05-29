import pandas as pd
import tkinter as tk
import sqlite3

conn = sqlite3.connect('cadastro.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS produto (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        preco REAL NOT NULL)
''')
conn.commit()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS venda (
        id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_id INTEGER NOT NULL,
        quantidade INTEGER NOT NULL,
        FOREIGN KEY (produto_id) REFERENCES produto (id))
''')
conn.commit()
conn.close()