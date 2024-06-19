import sqlite3

# Conectar a la base de datos SQLite (esto creará la base de datos si no existe)
conn = sqlite3.connect('casos.db')
cursor = conn.cursor()

# Crear la tabla de casos si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS casos (
        id INTEGER PRIMARY KEY,
        descripcion TEXT
    )
''')

# Confirmar los cambios
conn.commit()

# Cerrar la conexión
conn.close()

print("Base de datos y tabla 'casos' creadas exitosamente.")
