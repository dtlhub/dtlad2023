import sqlite3
import multiprocessing
import threading

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=Singleton):
    def __new__(cls):
        #pizdec ochen mnogo singltona
        if not hasattr(cls, 'instance'):
            cls.instance = super(Database, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        self.sem = threading.Semaphore()
        self.connection = sqlite3.connect('users.db', check_same_thread=False)
        cur = self.connection.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            flag TEXT)
                    """)
        self.connection.commit()
        cur.close()

    def register(self, username: str, password: str, flag: str) -> bool:
        try:
            self.sem.acquire()
            cur = self.connection.cursor()
            cur.execute(
            """
                INSERT INTO users(username, password, flag) VALUES(?,?,?);
            """, [username, password, flag])
            self.connection.commit()
            cur.close()
            self.sem.release()
            return True
        except Exception as e:
            print(str(e))
            return False

    def login(self, username: str, password: str) -> bool:
        cur = self.connection.cursor()
        cur.execute("SELECT password FROM users WHERE username=(?)", [username])
        data = cur.fetchone()
        cur.close()
        if data is None:
            return False

        return password == data[0]

    def get_flag(self, username: str) -> str:
        cur = self.connection.cursor()
        cur.execute("SELECT flag FROM users WHERE username=(?)", [username])
        data = cur.fetchone()
        cur.close()

        return data[0]
