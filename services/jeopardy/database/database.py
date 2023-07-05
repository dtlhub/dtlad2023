import sqlite3

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=Singleton):
    def __init__(self) -> None:
        self.connection = sqlite3.connect('users.db', check_same_thread=False)
        cur = self.connection.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            flag TEXT,
        )""")
        self.connection.commit()
        cur.close()

    def register(self, username: str, password: str, flag: str) -> bool:
        try:
            cur = self.connection.cursor()
            cur.execute(
            """
                INSERT INTO users(username, secret_key, hello_message, secret_message) VALUES(?,?,?,?);
            """, [username, secret_key, hello_message, secret_message])
            self.connection.commit()
            cur.close()
            return True
        except Exception as e:
            return False

    def login(self, username: str, password: str) -> bool:
        cur = self.connection.cursor()
        cur.execute("SELECT password FROM users WHERE username=(?)", [username])
        data = cur.fetchone()
        cur.close()
        if data is None:
            return False
        _, username, dbpassword, flag = data
        return password == dbpassword

    def get_flag(self, username: str) -> str:
        cur = self.connection.cursor()
        cur.execute("SELECT password FROM users WHERE username=(?)", [username])
        data = cur.fetchone()
        cur.close()
        if data is None:
            return False
        _, username, dbpassword, flag = data
        return flag
