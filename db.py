import sqlite3, time
from datetime import timedelta, datetime


class Database():
    def __init__(self):
        self.connection = sqlite3.connect("database.db", check_same_thread=False)
        self.cursor = self.connection.cursor()
    
    def user_exists(self, user_id):
        with self.connection:
            resp = self.cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id, )).fetchone()
        return bool(resp)

    def add_user(self, user_id, username):
        with self.connection:
            self.cursor.execute("INSERT INTO users(user_id, username) VALUES(?, ?)", (user_id, "@" + str(username),))
    
    def set_access(self, user_id, email):
        start = int(time.time())
        with self.connection:
            self.cursor.execute("UPDATE users SET email=?, has_access=1, sub_end=? WHERE user_id=?", (email, start + timedelta(days=7).total_seconds(), user_id, ))

    def has_access(self, user_id):
        with self.connection:
            resp = self.cursor.execute("SELECT sub_end FROM users WHERE user_id=?", (user_id, )).fetchone()
        return int(resp[0]) - int(time.time()) > 0

    def is_notified(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT is_notified FROM users WHERE user_id=?", (user_id, )).fetchone()[0] == 1

    def get_users_with_overdue_sub(self):
        with self.connection:
            res = self.cursor.execute("SELECT user_id, email, sub_end FROM users WHERE sub_end<>'0'").fetchall()
        return filter(lambda t: int(time.time()) - int(t[-1]) >= 0 and not self.is_notified(t[0]), res)


    def set_notified(self, user_id, status):
        with self.connection:
            self.cursor.execute("UPDATE USERS SET is_notified=? WHERE user_id=?", (int(status), user_id))

    def get_all_users(self):
        with self.connection:
            data = list(map(list, self.cursor.execute("SELECT id, user_id, username, email, sub_end FROM users").fetchall()))
        for user in data:
            for i in range(len(user)):
                user[i] = "" if user[i] in ("@None", None) else user[i]
            tg_id = user[1]
            user.insert(3, self.has_access(tg_id))
            user[-1] = str(timedelta(seconds=int(user[-1]) - time.time()))[:-7] if self.has_access(tg_id) else "Нет подписки"
        return data



# db = Database()
# d = time.time() + timedelta(days=7, hours=4, minutes=20, seconds=45).total_seconds() - time.time()
# print(db.get_all_users())
# db.set_access(818525681)
# print(*db.get_users_with_overdue_sub())
# print(db.has_access(818525681))

