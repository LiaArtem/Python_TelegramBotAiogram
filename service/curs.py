import os
import json
import sqlite3
import urllib.request
import xmltodict
import redis
from settings import settings


# Функция получения курсов валют
class Read_curs:
    def __init__(self, update_date, curr_code):
        if settings.bots.IS_WORK_REDIS_DB:
            p = Read_curs_Redis(update_date, curr_code)
        else:
            p = Read_curs_SQLite(update_date, curr_code)
        self.curs_amount = p.curs_amount
        self.curr_name = p.curr_name
        self.is_request_curs = p.is_request_curs
        self.text_error = p.text_error


class Read_curs_Redis:
    def __init__(self, update_date, curr_code):
        self.is_request_curs = True
        self.curs_amount = 0.00
        self.curr_name = ""
        self.text_error = ""
        try:
            r = redis.Redis(host=settings.bots.REDIS_HOST, port=settings.bots.REDIS_PORT, db=settings.bots.REDIS_CURS_DB_NO)
            if r.exists("UPDATE_DATE"):
                update_date_db = r.get("UPDATE_DATE").decode('utf-8')
                if update_date_db == update_date.strftime("%Y-%m-%d"):
                    if r.exists(curr_code):
                        data = json.loads(r.get(curr_code))
                        if len(data) > 0:
                            self.curs_amount = data["rate"]
                            self.curr_name = data["name"]
                            self.is_request_curs = False
                        else:
                            return  # курс не найден

            if self.is_request_curs:
                file_settings = './database/settings_curs_nbu.json'
                if not os.path.isfile(file_settings):
                    self.text_error = "File './database/settings_curs_nbu.json' not found"
                    print(self.text_error)
                    return

                # Opening JSON file
                f = open(file='./database/settings_curs_nbu.json', mode="r", encoding="utf8")
                data = json.loads(f.read())
                f.close()
                data_format = data['main']['data_format']
                if data_format == 'json':
                    url = data['main']['curs_nbu_json']['url']
                    char_curr_code = data['main']['curs_nbu_json']['char_curr_code']
                    char_curr_name = data['main']['curs_nbu_json']['char_curr_name']
                    char_curs = data['main']['curs_nbu_json']['char_curs']
                    char_format_date = data['main']['curs_nbu_json']['char_format_date']
                elif data_format == 'xml':
                    url = data['main']['curs_nbu_xml']['url']
                    char_curr_code = data['main']['curs_nbu_xml']['char_curr_code']
                    char_curr_name = data['main']['curs_nbu_xml']['char_curr_name']
                    char_curs = data['main']['curs_nbu_xml']['char_curs']
                    char_format_date = data['main']['curs_nbu_xml']['char_format_date']
                else:
                    self.text_error = "File 'settings_curs_nbu.json' -> parameter 'data_format' not in 'xml' or 'json'"
                    print(self.text_error)
                    return

                # Read url
                url = url.replace("%MDATE%", update_date.strftime(char_format_date)).replace("%CURRCODE%", curr_code)
                webURL = urllib.request.urlopen(url)
                data = webURL.read()

                if data_format == 'json':
                    JSON_object = json.loads(data.decode('utf-8'))
                    # write data
                    pipe = r.pipeline()
                    for json_line in JSON_object:
                        m_json = {"name": json_line[char_curr_name], "rate": json_line[char_curs]}
                        pipe.set(json_line[char_curr_code], json.dumps(m_json))
                    pipe.execute()
                elif data_format == 'xml':
                    JSON_object = xmltodict.parse(data.decode('utf-8'))
                    # write data
                    pipe = r.pipeline()
                    for json_line in JSON_object["exchange"]["currency"]:
                        m_json = {"name": json_line[char_curr_name], "rate": json_line[char_curs]}
                        pipe.set(json_line[char_curr_code], json.dumps(m_json))
                    pipe.execute()

                r.set("UPDATE_DATE", update_date.strftime("%Y-%m-%d"))

                # читаем снова
                if r.exists("UPDATE_DATE"):
                    update_date_db = r.get("UPDATE_DATE").decode('utf-8')
                    if update_date_db == update_date.strftime("%Y-%m-%d"):
                        if r.exists(curr_code):
                            data = json.loads(r.get(curr_code))
                            if len(data) > 0:
                                self.curs_amount = data["rate"]
                                self.curr_name = data["name"]
                                self.is_request_curs = False
                            else:
                                return  # курс не найден

        except Exception as err_curs:
            self.text_error = err_curs
            print(self.text_error)


class Read_curs_SQLite:
    def __init__(self, update_date, curr_code):
        self.is_request_curs = True
        self.curs_amount = 0.00
        self.curr_name = ""
        self.text_error = ""
        try:
            file_settings = './database/settings_curs_nbu.json'
            if not os.path.isfile(file_settings):
                self.text_error = "File './database/settings_curs_nbu.json' not found"
                print(self.text_error)
                return

            # Opening JSON file
            f = open(file='./database/settings_curs_nbu.json', mode="r", encoding="utf8")
            data = json.loads(f.read())
            f.close()
            data_format = data['main']['data_format']
            if data_format == 'json':
                url = data['main']['curs_nbu_json']['url']
                char_curr_code = data['main']['curs_nbu_json']['char_curr_code']
                char_curr_name = data['main']['curs_nbu_json']['char_curr_name']
                char_curs = data['main']['curs_nbu_json']['char_curs']
                char_format_date = data['main']['curs_nbu_json']['char_format_date']
            elif data_format == 'xml':
                url = data['main']['curs_nbu_xml']['url']
                char_curr_code = data['main']['curs_nbu_xml']['char_curr_code']
                char_curr_name = data['main']['curs_nbu_xml']['char_curr_name']
                char_curs = data['main']['curs_nbu_xml']['char_curs']
                char_format_date = data['main']['curs_nbu_xml']['char_format_date']
            else:
                self.text_error = "File 'settings_curs_nbu.json' -> parameter 'data_format' not in 'xml' or 'json'"
                print(self.text_error)
                return

            con = None
            try:
                # connect sqlite3
                con = sqlite3.connect("./database/currency.db")
                cursor = con.cursor()
                cursor.execute("""CREATE TABLE IF NOT EXISTS CURS
                                (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,  
                                 CURS_DATE INTEGER NOT NULL, 
                                 CURR_CODE TEXT NOT NULL,
                                 RATE REAL NOT NULL CHECK(RATE > 0),
                                 FORC INTEGER NOT NULL CHECK(FORC > 0)
                                 )
                            """)
                cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS UK_CURS ON CURS (CURS_DATE, CURR_CODE)")

                cursor.execute("""CREATE TABLE IF NOT EXISTS CURRENCY
                                (CURR_CODE TEXT NOT NULL,
                                 CURR_NAME TEXT)
                            """)
                cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS UK_CURRENCY ON CURRENCY (CURR_CODE)")

                # check curs
                self.is_request_curs = True
                params = (update_date.strftime("%Y-%m-%d"), curr_code)
                cursor.execute("SELECT K.RATE/K.FORC AS CURS_AMOUNT, C.CURR_NAME "
                               "FROM CURS K, CURRENCY C "
                               "WHERE K.CURR_CODE = C.CURR_CODE AND K.CURS_DATE = ? AND K.CURR_CODE = ?", params)
                rows = cursor.fetchall()
                for row in rows:
                    self.curs_amount = float(row[0])
                    self.curr_name = row[1]
                    self.is_request_curs = False

                if self.is_request_curs:
                    # Read url
                    url = url.replace("%MDATE%", update_date.strftime(char_format_date)).replace("%CURRCODE%",
                                                                                                 curr_code)
                    webURL = urllib.request.urlopen(url)
                    data = webURL.read()

                    if data_format == 'json':
                        JSON_object = json.loads(data.decode('utf-8'))
                        # write data
                        for json_line in JSON_object:
                            params = (update_date.strftime("%Y-%m-%d"),
                                      json_line[char_curr_code],
                                      json_line[char_curs],
                                      1)
                            cursor.execute(
                                "INSERT OR IGNORE INTO CURRENCY(curr_code, curr_name) VALUES(?, ?)",
                                (json_line[char_curr_code], json_line[char_curr_name]))
                            cursor.execute(
                                "INSERT OR IGNORE INTO CURS(curs_date, curr_code, rate, forc) VALUES(?, ?, ?, ?)",
                                params)
                    elif data_format == 'xml':
                        JSON_object = xmltodict.parse(data.decode('utf-8'))
                        # write data
                        json_line = JSON_object["exchange"]["currency"]
                        params = (update_date.strftime("%Y-%m-%d"),
                                  json_line[char_curr_code],
                                  json_line[char_curs],
                                  1)
                        cursor.execute("INSERT OR IGNORE INTO CURRENCY(curr_code, curr_name) VALUES(?, ?)",
                                       (json_line[char_curr_code], json_line[char_curr_name]))
                        cursor.execute("INSERT OR IGNORE INTO CURS(curs_date, curr_code, rate, forc) "
                                       "VALUES(?, ?, ?, ?)", params)

                    # read new curs
                    params = (update_date.strftime("%Y-%m-%d"), curr_code)
                    cursor.execute("SELECT K.RATE/K.FORC AS CURS_AMOUNT, C.CURR_NAME "
                                   "FROM CURS K, CURRENCY C "
                                   "WHERE K.CURR_CODE = C.CURR_CODE AND K.CURS_DATE = ? AND K.CURR_CODE = ?", params)
                    rows = cursor.fetchall()
                    for row in rows:
                        self.curs_amount = float(row[0])
                        self.curr_name = row[1]
                        self.is_request_curs = False

                con.commit()
                con.close()
            except Exception as err_curs:
                con.close()
                self.text_error = err_curs
                print(self.text_error)
        except Exception as err_curs:
            self.text_error = err_curs
            print(self.text_error)
