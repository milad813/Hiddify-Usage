import sqlite3

connection = sqlite3.connect('/opt/hiddify-manager/hiddify-panel/hiddifypanel.db')

cursor = connection.cursor()
query = f"select enable from user where name='Dadash'"
cursor.execute(query)
status = cursor.fetchone()

if status[0] == 0:
    query = f"UPDATE user SET enable = 1 WHERE name = 'Dadash'"
else:
    query = f"UPDATE user SET enable = 0 WHERE name = 'Dadash'"

cursor.execute(query)
connection.commit()
connection.close()