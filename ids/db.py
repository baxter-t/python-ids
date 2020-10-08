import mysql.connector

db = mysql.connector.connect(
    host="db",
    user="root",
    password="root",
    database="traffic"
)

dbcursor = db.cursor()

dbcursor.execute("SHOW TABLES")

if not "packets" in dbcursor
    dbcursor.execute("CREATE TABLE packets (src VARCHAR(255), dst VARCHAR(255))")
