import sqlite3

def create_database():
    # Conectar a la base de datos (la crea si no existe)
    conn = sqlite3.connect('users.db')

    # Crear un cursor para ejecutar comandos SQL
    cursor = conn.cursor()

    # Crear una tabla
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Guardar los cambios y cerrar la conexión
    conn.commit()
    conn.close()

create_database()
