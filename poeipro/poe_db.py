import sqlite3
import os.path
import time
from _thread import *

class DB:
    def __init__(self, db_file):
        self.lock = allocate_lock()
        self.conn = None

        if not os.path.exists(db_file):
            self.create_db_file(db_file)
        else:
            self.create_connection(db_file)

    def stop():
        self.conn.close()

    def upload(self, data):
        self.lock.acquire()
        try:
            self.conn.cursor().execute(
                        """INSERT OR REPLACE INTO sensors 
                        (ip_id, sensor, value, time) 
                        VALUES(?, ?, ?, ?)
                        """,
                        data)
            self.conn.commit()
        except Exception as e:
            print(e)
            print('[ERROR]:db_upload_error')
        self.lock.release()

    def create_connection(self, db_file):
        try:
            self.conn = sqlite3.connect(db_file, check_same_thread=False)
            print("connected to SQLite")
        except OSError as e:
            print(e)

    def create_db_file(self, db_file):
        table = """ CREATE TABLE IF NOT EXISTS sensors (
                ip_id TEXT PRIMARY KEY NOT NULL,
                sensor TEXT NOT NULL,
                value INTEGER NOT NULL,
                time REAL NOT NULL
            ); """

        with open(db_file, 'w') as fp:
            pass

        try:
            self.conn = sqlite3.connect(db_file, check_same_thread=False)
            c = self.conn.cursor()
            c.execute(table)
            print("db missing, created new db, connected to SQLite")
        except OSError as e:
            print(e)