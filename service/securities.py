import csv
import json
import logging
import aiosqlite
import urllib.request
import urllib.error
import redis.asyncio as redis
from datetime import datetime
from settings import settings


def get_name_securities_type(securities_type: str):
    m = {
        '1': 'Довгострокові',
        '2': 'Довгострокові з індексованою вартістю',
        '3': 'Довгострокові інфляційні',
        '4': 'Середньострокові',
        '5': 'Короткострокові дисконтні',
        '6': 'OЗДП%'
    }
    try:
        securities_name = m[securities_type]
    except Exception as err:
        securities_name = securities_type
        logging.error(err)  # логирование
    return securities_name


def get_code_securities_type(securities_type_name: str):
    if securities_type_name == 'Довгострокові':
        securities_code = '1'
    elif securities_type_name == 'Довгострокові з індексованою вартістю':
        securities_code = '2'
    elif securities_type_name == 'Довгострокові інфляційні':
        securities_code = '3'
    elif securities_type_name == 'Середньострокові':
        securities_code = '4'
    elif securities_type_name == 'Короткострокові дисконтні':
        securities_code = '5'
    elif securities_type_name.startswith('OЗДП'):
        securities_code = '6'
    else:
        securities_code = '7'
    return securities_code


def get_str_isin_from_json(m_json, m_fair_json, m_is_coup_period: bool):
    buff = ""
    if m_json is not None:
        if m_fair_json is not None:
            if m_fair_json.get('fair_date') is None:
                fair_value = "--"
            else:
                if (m_fair_json.get('fair_date') is None or
                        m_fair_json.get('fair_date') == datetime.now().strftime("%Y-%m-%d")):
                    fair_value = str(m_fair_json.get('fair_value'))
                else:
                    fair_value = str(m_fair_json.get('fair_value')) + " за " + str(m_fair_json.get('fair_date'))
        else:
            fair_value = "--"

        buff = ("ISIN: " + str(m_json.get('cpcode')) + "\n"
                + "Номінал: " + str(m_json.get('nominal')) + "\n"
                + "Вартість: " + fair_value + "\n"
                + "Валюта: " + str(m_json.get('val_code')) + "\n"
                + "% ставка: " + str(m_json.get('auk_proc')) + "\n"
                + "Дата виплати: " + str(m_json.get('pgs_date')) + "\n"
                )

        if m_is_coup_period:
            for num, coup in enumerate(m_json.get('payments')):
                if num == 0:
                    buff = buff + "Купонні періоди:" + "\n"
                if coup.get('pay_type') == '1':
                    buff = buff + "- " + str(coup.get('pay_date')) + " = " + str(coup.get('pay_val')) + "\n"
    return buff


# Функция получения данных о ценных бумагах
class Read_ISIN_Securities:
    def __init__(self, securities_type, curr_code, securities_isin, is_coup_period):
        self.securities_type = securities_type
        self.curr_code = curr_code
        self.securities_isin = securities_isin
        self.is_coup_period = is_coup_period
        self.text_result = ""
        self.is_error = False

    async def get_Read_ISIN_Securities(self):
        # db Redis
        if settings.bots.IS_WORK_REDIS_DB:
            r = None
            try:
                r = redis.Redis(host=settings.bots.REDIS_HOST,
                                port=settings.bots.REDIS_PORT,
                                db=settings.bots.REDIS_SECURITIES_DB_NO)
                # main
                is_load_data = False
                if await r.exists("UPDATE_DATE"):
                    update_date_db_binary = await r.get("UPDATE_DATE")
                    update_date_db = update_date_db_binary.decode('utf-8')
                    if update_date_db == datetime.now().strftime("%Y-%m-%d"):
                        is_load_data = True

                if not is_load_data:
                    data = urllib.request.urlopen("https://bank.gov.ua/depo_securities?json").read()
                    # write data
                    mas = []
                    pipe = await r.pipeline()
                    for num, json_line in enumerate(json.loads(data.decode('utf-8'))):
                        await pipe.set(json_line['cpcode'], json.dumps(json_line))
                        key = ('TYPE_' + str(get_code_securities_type(json_line['cpdescr'])) +
                               '_' + json_line['val_code'])

                        if len(mas) == 0:
                            dr = {key: {json_line['cpcode']}}
                            mas.append(dr)
                        else:
                            is_exists_dr = False
                            for num_dr, data_dr in enumerate(mas):
                                dr = data_dr
                                if dr.get(key) is not None:
                                    u = dr.get(key)
                                    u.update({json_line['cpcode']})
                                    dr[key] = u
                                    mas[num_dr] = dr
                                    is_exists_dr = True
                            if not is_exists_dr:
                                dr = {key: {json_line['cpcode']}}
                                mas.append(dr)
                    await pipe.execute()
                    # список json по типам
                    for dr in mas:
                        keys = list(dr.keys())
                        data = str(dr.get(keys[0]))
                        removed_chars = ["'", "{", "}", " "]
                        chars = set(removed_chars)
                        data = ''.join(c for c in data if c not in chars)
                        await r.set(keys[0], data)
                    await r.set("UPDATE_DATE", datetime.now().strftime("%Y-%m-%d"))

                # fair
                is_load_data = False
                if await r.exists("UPDATE_DATE_FAIR"):
                    update_date_db_binary = await r.get("UPDATE_DATE_FAIR")
                    update_date_db = update_date_db_binary.decode('utf-8')
                    if update_date_db == datetime.now().strftime("%Y-%m-%d"):
                        is_load_data = True

                if not is_load_data:
                    try:
                        url = "https://bank.gov.ua/files/Fair_value/" + datetime.now().strftime(
                            "%Y%m") + "/" + datetime.now().strftime("%Y%m%d") + "_fv.txt"
                        response = urllib.request.urlopen(url)
                        lines = [line.decode('cp1251') for line in response.readlines()]
                        cr = csv.reader(lines)
                        pipe = await r.pipeline()
                        for row in cr:
                            split_data = row[0].split(";")
                            if split_data[1] == "cpcode":
                                continue
                            m_json = {"fair_date": datetime.now().strftime("%Y-%m-%d"),
                                      "fair_value": float(split_data[3])}
                            await pipe.set(split_data[1] + '_FAIR', json.dumps(m_json))
                        await pipe.execute()
                        await r.set("UPDATE_DATE_FAIR", datetime.now().strftime("%Y-%m-%d"))
                    except urllib.error.HTTPError as e:
                        if e.code != 404:
                            raise

                # поиск по ISIN
                if self.securities_isin != "":
                    key = self.securities_isin
                    if await r.exists(key):
                        data = json.loads(await r.get(key))
                        data_fair = None
                        if await r.exists(key + '_FAIR'):
                            data_fair = json.loads(await r.get(key + '_FAIR'))
                        self.text_result = get_str_isin_from_json(data, data_fair, self.is_coup_period)
                    else:
                        return self  # не найдено
                else:
                    # поиск по типу и валюте
                    key = 'TYPE_' + self.securities_type + '_' + self.curr_code
                    if await r.exists(key):
                        dr_binary = await r.get(key)
                        dr = dr_binary.decode('utf-8').split(",")
                        for isin in dr:
                            if await r.exists(isin):
                                data = json.loads(await r.get(isin))
                                data_fair = None
                                if await r.exists(isin + '_FAIR'):
                                    data_fair = json.loads(await r.get(isin + '_FAIR'))
                                self.text_result = (self.text_result + "\n" +
                                                    get_str_isin_from_json(data, data_fair, self.is_coup_period))
                    else:
                        return self  # не найдено

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
                db = await aiosqlite.connect("./database/securities.db")
                await db.execute("""CREATE TABLE IF NOT EXISTS SECUR_ISIN
                                (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,                               
                                 ISIN TEXT NOT NULL,
                                 NOMINAL INTEGER NOT NULL,
                                 AUK_PROC REAL NOT NULL,
                                 PGS_DATE INTEGER NOT NULL,
                                 CPDESCR TEXT NOT NULL,
                                 CURRENCY_CODE TEXT NOT NULL,
                                 SDATE INTEGER NOT NULL,
                                 FAIR_DATE INTEGER,
                                 FAIR_VALUE REAL
                                 )
                            """)
                await db.execute("CREATE UNIQUE INDEX IF NOT EXISTS UK_SECUR_ISIN ON SECUR_ISIN (ISIN)")

                await db.execute("""CREATE TABLE IF NOT EXISTS SECUR_ISIN_PAY
                                (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,                               
                                 ISIN_SECUR_ID INTEGER NOT NULL,
                                 PAY_DATE INTEGER NOT NULL,
                                 PAY_TYPE INTEGER NOT NULL,
                                 PAY_VAL REAL NOT NULL,
                                 FOREIGN KEY(ISIN_SECUR_ID) REFERENCES SECUR_ISIN(ID)                           
                                 )
                            """)
                await db.execute("CREATE UNIQUE INDEX IF NOT EXISTS UK_SECUR_ISIN_PAY ON SECUR_ISIN_PAY "
                                 "(ISIN_SECUR_ID,PAY_DATE, PAY_TYPE)")

                # проверяем есть ли обновленные данные по ISIN ЦБ за текущий день, если нет перезаливаем
                params = (datetime.now().strftime("%Y-%m-%d"),)
                cursor = await db.execute("SELECT COUNT(*) AS KOL FROM SECUR_ISIN S WHERE S.SDATE = ?", params)
                rows = await cursor.fetchone()
                # если нет данных загрузить их
                if rows[0] == 0:
                    data = urllib.request.urlopen("https://bank.gov.ua/depo_securities?json").read()
                    # write data
                    for json_line in json.loads(data.decode('utf-8')):
                        # возвращаем ID
                        params = (json_line['cpcode'],)
                        cursor = await db.execute(
                            "SELECT COUNT(*) AS KOL, MAX(ID) AS ID FROM SECUR_ISIN S WHERE S.ISIN = ?", params)
                        rows = await cursor.fetchone()
                        if rows[0] == 0:
                            params = (json_line['cpcode'],
                                      json_line['nominal'],
                                      json_line['auk_proc'],
                                      json_line['pgs_date'],
                                      json_line['cpdescr'],
                                      json_line['val_code'],
                                      datetime.now().strftime("%Y-%m-%d")
                                      )
                            await db.execute(
                                'INSERT INTO SECUR_ISIN(ISIN, NOMINAL, AUK_PROC, PGS_DATE, CPDESCR, CURRENCY_CODE, '
                                'SDATE) VALUES(?, ?, ?, ?, ?, ?, ?)', params)

                            params = (json_line['cpcode'],)
                            cursor = await db.execute(
                                "SELECT COUNT(*) AS KOL, MAX(ID) AS ID FROM SECUR_ISIN S WHERE S.ISIN = ?",
                                params)
                            rows = await cursor.fetchone()
                            inserted_id = rows[1]
                        else:
                            inserted_id = rows[1]
                            params = (datetime.now().strftime("%Y-%m-%d"),
                                      inserted_id)
                            await db.execute(
                                'UPDATE SECUR_ISIN SET SDATE = ? WHERE ID = ?', params)

                        # купонные периоды
                        for json_line2 in json_line['payments']:
                            params = (inserted_id,
                                      json_line2['pay_date'],
                                      json_line2['pay_type'],
                                      json_line2['pay_val']
                                      )
                            await db.execute(
                                "INSERT OR IGNORE INTO SECUR_ISIN_PAY(ISIN_SECUR_ID, PAY_DATE, PAY_TYPE, PAY_VAL) "
                                "VALUES(?, ?, ?, ?)", params)

                # Справедливая стоимость ЦБ (котировки НБУ)
                params = (datetime.now().strftime("%Y-%m-%d"),)
                cursor = await db.execute("SELECT COUNT(*) AS KOL FROM SECUR_ISIN S WHERE S.FAIR_DATE = ?", params)
                rows = await cursor.fetchone()
                # если нет данных загрузить их и обновить
                if rows[0] == 0:
                    try:
                        url = "https://bank.gov.ua/files/Fair_value/" + datetime.now().strftime(
                            "%Y%m") + "/" + datetime.now().strftime("%Y%m%d") + "_fv.txt"
                        response = urllib.request.urlopen(url)
                        lines = [line.decode('cp1251') for line in response.readlines()]
                        cr = csv.reader(lines)
                        for row in cr:
                            split_data = row[0].split(";")
                            if split_data[1] == "cpcode":
                                continue
                            params = (datetime.now().strftime("%Y-%m-%d"),
                                      float(split_data[3]),
                                      split_data[1])
                            await db.execute(
                                'UPDATE SECUR_ISIN SET FAIR_DATE = ?, FAIR_VALUE = ? WHERE ISIN = ?', params)
                    except urllib.error.HTTPError as e:
                        if e.code != 404:
                            raise
                # Получить данные
                if self.securities_isin == "":
                    securities_name = get_name_securities_type(self.securities_type)
                    params = (securities_name, self.curr_code)
                    if securities_name.find("%") >= 0:
                        cursor = await db.execute("SELECT * FROM SECUR_ISIN S WHERE S.CPDESCR like ? AND "
                                                  "S.CURRENCY_CODE = ?", params)
                    else:
                        cursor = await db.execute("SELECT * FROM SECUR_ISIN S WHERE S.CPDESCR = ? AND S.CURRENCY_CODE "
                                                  "= ?", params)
                    rows = await cursor.fetchall()
                else:
                    params = (self.securities_isin,)
                    cursor = await db.execute("SELECT * FROM SECUR_ISIN S WHERE S.ISIN = ?", params)
                    rows = await cursor.fetchall()
                buff = ""
                for row_count, row in enumerate(rows):
                    if row[9] is None:
                        fair_value = "--"
                    else:
                        if row[8] is None or row[8] == datetime.now().strftime("%Y-%m-%d"):
                            fair_value = str(row[9])
                        else:
                            fair_value = str(row[9]) + " за " + str(row[8])
                    buff = buff + ("ISIN: " + str(row[1]) + "\n"
                                   + "Номінал: " + str(row[2]) + "\n"
                                   + "Вартість: " + fair_value + "\n"
                                   + "Валюта: " + str(row[6]) + "\n"
                                   + "% ставка: " + str(row[3]) + "\n"
                                   + "Дата виплати: " + str(row[4]) + "\n"
                                   )
                    # купонные периоды
                    if self.is_coup_period:
                        params = (row[0],)
                        cursor = await db.execute(
                            "SELECT * FROM SECUR_ISIN_PAY S WHERE S.ISIN_SECUR_ID = ? AND S.PAY_TYPE = 1 "
                            "ORDER BY S.PAY_DATE",
                            params)
                        rows2 = await cursor.fetchall()
                        if rows2 is not None:
                            buff = buff + "Купонні періоди:" + "\n"
                        for row2 in rows2:
                            buff = buff + "- " + str(row2[2]) + " = " + str(row2[4]) + "\n"
                    buff = buff + "\n"

                await db.commit()
                await db.close()

                self.text_result = buff
            except Exception as err_message:
                if db is not None:
                    await db.close()
                self.is_error = True
                logging.error(err_message)  # логирование

        return self
