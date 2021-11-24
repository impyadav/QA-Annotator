import sqlite3 as sql
import sqlite3

conn = sqlite3.connect('database.db')
print("Opened database successfully")

# conn.execute('CREATE TABLE annoatations (paraid TEXT, doc_id TEXT, content TEXT, status TEXT, datetime DATETIME)')
# conn.execute('CREATE TABLE questList (paraid TEXT, ques_id TEXT, ques TEXT, ans TEXT)')
# print("Table created successfully")
# conn.close()


