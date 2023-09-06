import aiosqlite


class User_DB_Request:
    def __init__(self, db: aiosqlite.Connection):
        self.db = db

    async def create_table(self):
        await self.db.execute("""CREATE TABLE IF NOT EXISTS USERS
                            (USER_ID INTEGER PRIMARY KEY NOT NULL, 
                             USER_NAME TEXT
                             )""")

    async def add_data(self, user_id, user_name):
        await self.db.execute("INSERT OR IGNORE INTO USERS (USER_ID, USER_NAME) VALUES (?, ?)", (user_id, user_name))
        await self.db.commit()
