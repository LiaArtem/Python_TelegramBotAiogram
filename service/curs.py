import json
import logging
import aiosqlite
import urllib.request
import redis.asyncio as redis
from settings import settings


# Функция получения курсов валют
class Read_curs:
    def __init__(self, update_date, curr_code):
        self.update_date = update_date
        self.curr_code = curr_code        
        self.curs_amount = 0.00
        self.curr_name = ""
        self.is_error = False

    async def get_Read_curs(self):
        # db Redis
        if settings.bots.IS_WORK_REDIS_DB:
            r = None
            try:
                r = redis.Redis(host=settings.bots.REDIS_HOST,
                                port=settings.bots.REDIS_PORT,
                                db=settings.bots.REDIS_CURS_DB_NO)

                is_load_data = False
                if await r.exists("UPDATE_DATE"):
                    update_date_db_binary = await r.get("UPDATE_DATE")
                    update_date_db = update_date_db_binary.decode('utf-8')
                    if update_date_db == self.update_date.strftime("%Y-%m-%d"):
                        is_load_data = True
                        
                if not is_load_data:
                    # Read url
                    url = (f"https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?"
                           f"date={self.update_date.strftime('%Y%m%d')}&json")
                    data = urllib.request.urlopen(url).read()
                    # write data
                    pipe = await r.pipeline()
                    for json_line in json.loads(data.decode('utf-8')):
                        m_json = {"name": json_line['txt'], "rate": json_line['rate']}
                        await pipe.set(json_line['cc'], json.dumps(m_json))
                    await pipe.execute()
                    await r.set("UPDATE_DATE", self.update_date.strftime("%Y-%m-%d"))
                    
                # читаем            
                if await r.exists(self.curr_code):
                    data = json.loads(await r.get(self.curr_code))
                    if len(data) > 0:
                        self.curs_amount = data["rate"]
                        self.curr_name = data["name"]                        
                    else:
                        return self  # курс не найден

                await r.close()
            except Exception as err_message:
                if r is not None:
                    await r.close()
                self.is_error = True
                logging.error(err_message)  # логирование
        else:
            # db SQLite
            db = None
            try:
                # connect sqlite3
                db = await aiosqlite.connect("./database/currency.db")
                await db.execute("""CREATE TABLE IF NOT EXISTS CURS
                                (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,  
                                 CURS_DATE INTEGER NOT NULL, 
                                 CURR_CODE TEXT NOT NULL,
                                 RATE REAL NOT NULL CHECK(RATE > 0),
                                 FORC INTEGER NOT NULL CHECK(FORC > 0)
                                 )
                            """)
                await db.execute("CREATE UNIQUE INDEX IF NOT EXISTS UK_CURS ON CURS (CURS_DATE, CURR_CODE)")

                await db.execute("""CREATE TABLE IF NOT EXISTS CURRENCY
                                (CURR_CODE TEXT NOT NULL,
                                 CURR_NAME TEXT)
                            """)
                await db.execute("CREATE UNIQUE INDEX IF NOT EXISTS UK_CURRENCY ON CURRENCY (CURR_CODE)")

                # check curs
                is_request_curs = True
                params = (self.update_date.strftime("%Y-%m-%d"), self.curr_code)
                cursor = await db.execute("SELECT K.RATE/K.FORC AS CURS_AMOUNT, C.CURR_NAME "
                                          "FROM CURS K, CURRENCY C "
                                          "WHERE K.CURR_CODE = C.CURR_CODE AND K.CURS_DATE = ? AND K.CURR_CODE = ?",
                                          params)
                rows = await cursor.fetchall()
                for row in rows:
                    self.curs_amount = float(row[0])
                    self.curr_name = row[1]
                    is_request_curs = False

                if is_request_curs:
                    # Read url
                    url = (f"https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?"
                           f"date={self.update_date.strftime('%Y%m%d')}&json")
                    data = urllib.request.urlopen(url).read()
                    # write data
                    for json_line in json.loads(data.decode('utf-8')):
                        params = (self.update_date.strftime("%Y-%m-%d"),
                                  json_line['cc'],
                                  json_line['rate'],
                                  1)
                        await db.execute(
                            "INSERT OR IGNORE INTO CURRENCY(curr_code, curr_name) VALUES(?, ?)",
                            (json_line['cc'], json_line['txt']))
                        await db.execute(
                            "INSERT OR IGNORE INTO CURS(curs_date, curr_code, rate, forc) VALUES(?, ?, ?, ?)",
                            params)
                        await db.commit()
                    # read new curs
                    params = (self.update_date.strftime("%Y-%m-%d"), self.curr_code)
                    cursor = await db.execute("SELECT K.RATE/K.FORC AS CURS_AMOUNT, C.CURR_NAME "
                                              "FROM CURS K, CURRENCY C "
                                              "WHERE K.CURR_CODE = C.CURR_CODE AND K.CURS_DATE = ? AND K.CURR_CODE = ?",
                                              params)
                    rows = await cursor.fetchall()
                    for row in rows:
                        self.curs_amount = float(row[0])
                        self.curr_name = row[1]

                await db.close()
            except Exception as err_message:
                if db is not None:
                    await db.close()
                self.is_error = True
                logging.error(err_message)  # логирование

        return self  # возвращаем параметры
