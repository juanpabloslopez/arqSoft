import socket
import sqlite3

def inicializar_bd():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()

    # Crear la tabla de usuarios si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            tipo TEXT NOT NULL
        )
    ''')

    # Crear la tabla de casos si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS casos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            descripcion TEXT NOT NULL,
            estado TEXT NOT NULL,
            lawyer_id INTEGER,
            FOREIGN KEY(client_id) REFERENCES usuarios(id),
            FOREIGN KEY(lawyer_id) REFERENCES usuarios(id)
        )
    ''')

    conn.commit()
    return conn, cursor

def manejar_registro(datos, cursor, conn):
    try:
        nombre, email, password, tipo = datos.split(maxsplit=3)
        if tipo not in ["client", "lawyer"]:
            return "Tipo de usuario no válido. Debe ser 'client' o 'lawyer'."
        
        cursor.execute("SELECT id FROM usuarios WHERE email = ?", (email,))
        if cursor.fetchone() is not None:
            return f"El usuario con email {email} ya existe."
        else:
            cursor.execute("INSERT INTO usuarios (nombre, email, password, tipo) VALUES (?, ?, ?, ?)", (nombre, email, password, tipo))
            conn.commit()
            return f"Usuario {nombre} ha sido registrado exitosamente."
    except Exception as e:
        return f"Error procesando registro: {e}"

def manejar_login(datos, cursor):
    try:
        email, password = datos.split(maxsplit=1)
        cursor.execute("SELECT id, tipo FROM usuarios WHERE email = ? AND password = ?", (email, password))
        usuario = cursor.fetchone()
        if usuario:
            return f"Login exitoso. ID: {usuario[0]}, Tipo: {usuario[1]}"
        else:
            return "Email o contraseña incorrectos."
    except Exception as e:
        return f"Error procesando login: {e}"

def manejar_subida_caso(datos, cursor, conn):
    try:
        client_id, descripcion = datos.split(maxsplit=1)
        cursor.execute("INSERT INTO casos (client_id, descripcion, estado) VALUES (?, ?, ?)", (client_id, descripcion, "disponible"))
        conn.commit()
        return "Caso subido exitosamente."
    except Exception as e:
        return f"Error procesando subida de caso: {e}"

def manejar_tomar_caso(datos, cursor, conn):
    try:
        lawyer_id, caso_id = datos.split(maxsplit=1)
        cursor.execute("UPDATE casos SET estado = ?, lawyer_id = ? WHERE id = ? AND estado = ?", ("tomado", lawyer_id, caso_id, "disponible"))
        if cursor.rowcount == 0:
            return "El caso no está disponible o no existe."
        conn.commit()
        return "Caso tomado exitosamente."
    except Exception as e:
        return f"Error procesando toma de caso: {e}"

# Inicializar base de datos
conn, cursor = inicializar_bd()

# Crear un socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar el socket al puerto donde el bus está escuchando
server_address = ('localhost', 5001)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Escuchar conexiones entrantes
sock.listen(1)

try:
    while True:
        print('waiting for a connection')
        connection, client_address = sock.accept()
        try:
            print('connection from', client_address)

            while True:
                # Recibir el encabezado
                header = connection.recv(5)
                if not header:
                    break
                amount_expected = int(header)

                # Recibir el resto del mensaje
                data = b""
                while len(data) < amount_expected:
                    chunk = connection.recv(amount_expected - len(data))
                    if not chunk:
                        break
                    data += chunk

                comando = data[:5].decode()
                datos = data[5:].decode()
                print(f"comando: {comando}, datos: {datos}")

                if comando == "regus":
                    respuesta = manejar_registro(datos, cursor, conn)
                elif comando == "login":
                    respuesta = manejar_login(datos, cursor)
                elif comando == "upcas":
                    respuesta = manejar_subida_caso(datos, cursor, conn)
                elif comando == "tkcas":
                    respuesta = manejar_tomar_caso(datos, cursor, conn)
                else:
                    respuesta = "Comando no reconocido."

                # Enviar respuesta
                response_length = len(respuesta)
                message = f"{response_length:05}".encode() + respuesta.encode()
                connection.sendall(message)
        finally:
            connection.close()
finally:
    conn.close()
    sock.close()

