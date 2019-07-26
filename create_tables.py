import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

query = "INSERT INTO meetings (group_id, topic, location, date_held) VALUES(1, 'First Meeting', 'Nairobi - West', '12-01-2019')"

query2 = """SELECT m.topic, m.location, m.date_held, g.name,
            (SELECT SUM(b.group_id) FROM members AS b WHERE b.group_id = m.group_id GROUP BY b.group_id)
            FROM meetings AS m
            JOIN groups AS g ON m.group_id = g.id
          """

query3 = ""

cursor.execute(query2)
res = cursor.fetchall()
print(res)

connection.commit()
connection.close()
