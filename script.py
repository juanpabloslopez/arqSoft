import sqlite3

conn = sqlite3.connect('usuarios.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM usuarios")
usuarios = cursor.fetchall()

print("Usuarios en la base de datos:")
for usuario in usuarios:
    print(usuario)

conn.close()
