import sqlite3



db = sqlite3.connect('server.db')
sql = db.cursor()


sql.execute("""CREATE TABLE IF NOT EXISTS users (
    ID INTEGER,
    NUMGROUP TEXT,
    CATEGORY TEXT,
    FORMSTATE TEXT,
    MAILING INTEGER
)""")

sql.execute("""CREATE TABLE IF NOT EXISTS tasks (
    DATE TEXT NOT NULL,
    NUMGROUP TEXT NOT NULL,
    CONTENTS TEXT NOT NULL
)""")

sql.execute("""CREATE TABLE IF NOT EXISTS contacts (
    FULLNAME TEXT,
    FIO TEXT,
    PHONENUMBER TEXT,
    TELEGRAM TEXT,
    MAIL TEXT
)""")

db.commit()
db.close()