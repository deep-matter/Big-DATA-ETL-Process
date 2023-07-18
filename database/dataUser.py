import sqlite3
from sqlite3 import Error
import sqlite3

try:
    sqliteConnection_user = sqlite3.connect('./dataUser.db')
    sqliteConnection_elt = sqlite3.connect("./dataETL.db")
    cursor = [sqliteConnection_user, sqliteConnection_elt]
    for create in cursor:
        cursor_ID = create.cursor()
        print("Database created and Successfully Connected to SQLite")
        sqlite_select_Query = "select sqlite_version();"
        cursor_ID.execute(sqlite_select_Query)
        record = cursor_ID.fetchall()
        print("SQLite Database Version is: ", record)
        cursor_ID.close()
except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)
finally:
    if cursor[0] and cursor[1]:
        cursor[0].close()
        cursor[1].close()
        print("The SQLite connection is closed")
