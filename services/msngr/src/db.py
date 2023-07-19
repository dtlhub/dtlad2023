import sqlite3
import threading



class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=Singleton):
    def __init__(self):
        self.connection = sqlite3.connect('data/users.db', check_same_thread=False)
        self.sem = threading.Semaphore()
        cur = self.connection.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            secret_key TEXT,
            hello_message TEXT,
            secret_message TEXT
        )"""
        )
        cur.close()

    # return 500 last users
    def users_list(self):
        cur = self.connection.cursor()
        cur.execute(
            """
            SELECT username FROM (
                SELECT id, username FROM users ORDER BY id DESC LIMIT 500
            ) ORDER BY id ASC;
        """
        )
        data = cur.fetchall()
        cur.close()
        return [i[0] for i in data]

    def add_user(self, username, secret_key, hello_message, secret_message):
        try:
            self.sem.acquire()
            cur = self.connection.cursor()
            cur.execute(
                """
                INSERT INTO users(username, secret_key, hello_message, secret_message) VALUES(?,?,?,?);
            """,
                [username, secret_key, hello_message, secret_message],
            )
            cur.close()
            self.sem.release()
            return "Succesfully registered", True
        except Exception as e:
            return str(e), False

    def get_user_info(self, username):
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username=(?)", [username])
        data = cur.fetchone()
        cur.close()
        if data is None:
            return []
        _, username, secret_key, hello_message, secret_message = data
        return [username, secret_key, hello_message, secret_message]
