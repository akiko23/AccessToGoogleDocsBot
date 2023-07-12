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
            self.cursor.execute("INSERT INTO users(user_id, has_access) VALUES(?, 0)", (user_id, ))
    
    def set_access(self, user_id):
        with self.connection:
            self.cursor.execute("UPDATE users SET access=1 WHERE user_id=?", (user_id, ))
        
    def reset_access(self):
        with self.connection:
            self.cursor.execute("UPDATE users SET has_access=0")

    def has_access(self, user_id):
        with self.connection:
            resp = self.cursor.execute("SELECT has_access FROM users WHERE user_id=?", (user_id, ))
        try:
            return bool(int(resp.fetchone()[0]))
        except:
            return False

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

    def add_payment(self, user_id, wallet):
        args = (user_id, wallet, int(time.time()) + timedelta(minutes=10).total_seconds())
        with self.connection:
            self.cursor.execute("UPDATE wallets SET status=1 WHERE wallet=?", (wallet, ))
            self.cursor.execute("INSERT INTO payments(user_id, wallet, timeout) VALUES(?, ?, ?)", args)



# db = Database()
# db.add_payment(123, "agkgkoAKO=1GAKG1wegamgaogek3-gjd")
# db.add_user(123)
# print(db.has_access(818525681))

