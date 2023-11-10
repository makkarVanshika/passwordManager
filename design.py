import hashlib
import random
import sqlite3
from getpass import getpass
import string
#from rich import print as printc

def generateDeviceSecret(length=10):
	return ''.join(random.choices(string.ascii_uppercase + string.digits, k = length))

def design():
    connection = sqlite3.connect('password.db')
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS secret (
            master_key TEXT NOT NULL,
            device TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entry (
            sitename INTEGER PRIMARY KEY,
            url TEXT NOT NULL,
            email TEXT,
            username TEXT,
            password TEXT NOT NULL
        )
    ''')

    while 1:
        master = getpass("Choose a master password: ")
        if master == getpass("Re-type: ") and master!="":
            break

    hashed_mp = hashlib.sha256(master.encode()).hexdigest()

    ds = generateDeviceSecret()

    cursor.execute('''
                   INSERT INTO secret (master_key, device)
                    VALUES (? , ?)
                ''', (hashed_mp, ds))
    connection.commit()
    connection.close()

design()
