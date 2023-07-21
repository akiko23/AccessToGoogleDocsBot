import sqlite3, time
from datetime import timedelta


class Database():
    def __init__(self):
        self.connection = sqlite3.connect("database.db", check_same_thread=False)
        self.cursor = self.connection.cursor()
    
    def user_exists(self, user_id):
        with self.connection:
            resp = self.cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id, )).fetchone()
        return bool(resp)

    def add_user(self, user_id):
        with self.connection:
            self.cursor.execute("INSERT INTO users(user_id) VALUES(?)", (user_id, ))
    
    def set_access(self, user_id, email):
        start = int(time.time())
        with self.connection:
            self.cursor.execute("UPDATE users SET email=?, sub_start=?, sub_end=? WHERE user_id=?", (email, start, start + timedelta(days=7).total_seconds(), user_id, ))

    def has_access(self, user_id):
        with self.connection:
            resp = self.cursor.execute("SELECT sub_end FROM users WHERE user_id=?", (user_id, )).fetchone()
        return int(resp[0]) - int(time.time()) > 0

    def add_wallet(self, address, coin):
        with self.connection():
            self.cursor.execute("INSERT INTO wallets(address, coin, status) VALUES(?, ?, 0)", (address, coin, ))
    
    def get_wallet_by_coin(self, coin, network=None):
        with self.connection:
            if network:
                return self.cursor.execute("SELECT address FROM wallets WHERE coin=? AND network=?", (coin, network, )).fetchone()[0]
            return self.cursor.execute("SELECT address FROM wallets WHERE coin=?", (coin, )).fetchone()[0]

    def get_free_wallets(self):
        with self.connection:
            # 0 - free, 1 - occupied
            return self.cursor.execute("SELECT address FROM wallets WHERE status=0").fetchall()

    def is_notified(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT is_notified FROM users WHERE user_id=?", (user_id, )).fetchone()[0] == 1

    def get_users_with_overdue_sub(self):
        with self.connection:
            res = self.cursor.execute("SELECT user_id, email, sub_end FROM users WHERE sub_start<>'0'").fetchall()
        return filter(lambda t: int(time.time()) - int(t[-1]) >= 0 and not self.is_notified(t[0]), res)


    def set_notified(self, user_id, status):
        with self.connection:
            self.cursor.execute("UPDATE USERS SET is_notified=? WHERE user_id=?", (int(status), user_id))



db = Database()
# db.set_access(818525681)
# print(*db.get_users_with_overdue_sub())
# print(db.has_access(818525681))

