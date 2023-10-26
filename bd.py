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
    DATE TEXT,
    NUMGROUP TEXT,
    SUBJECT TEXT,
    CONTENTS BLOB
)""")

db.commit()
db.close()