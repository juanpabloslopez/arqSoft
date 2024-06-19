import sqlite3

conn = sqlite3.connect('casos.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM casos")
casos = cursor.fetchall()

print("Casos en la base de datos:")
for caso in casos:
    print(caso)

conn.close()
