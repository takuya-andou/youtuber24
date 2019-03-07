import sqlite3
import subprocess

dbpath = 'mail.db'

connection = sqlite3.connect(dbpath)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()


cursor.execute('SELECT * FROM mail where read_flg = 0 ORDER BY sent_at')
row = cursor.fetchone()

print(row['uidl'])
print(row['subject'].replace(' by PR TIMES', ''))


# subprocess.call('say ' + '"' + row['subject'] + '"', shell=True)

# update read flag
cursor.execute("UPDATE mail SET read_flg = 1 where uidl = '" +
               row['uidl'] + "'")
connection.commit()
