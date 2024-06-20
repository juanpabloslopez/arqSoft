import socket
import sys
import sqlite3

# Crear un socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar el socket al puerto donde el bus está escuchando
bus_address = ('localhost', 5000)
print('connecting to {} port {}'.format(*bus_address))
sock.connect(bus_address)

# Conectar a la base de datos SQLite
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
conn.commit()

try:
    # Enviar datos de inicio
    message = b'00010sinitregus'
    print('sending {!r}'.format(message))
    sock.sendall(message)
    sinit = 1

    while True:
        # Esperar la transacción
        print("Waiting for transaction")
        amount_received = 0
        amount_expected = int(sock.recv(5))

        data = b""
        while amount_received < amount_expected:
            chunk = sock.recv(amount_expected - amount_received)
            amount_received += len(chunk)
            data += chunk
        print("Processing ...")
        print('received {!r}'.format(data))
        
        if sinit == 1:
            sinit = 0
            print('Received sinit answer')
        else:
            comando = data[:5].decode()
            datos = data[5:]
            if comando == "regus":
                try:
                    nombre, email, password, tipo = datos.split(maxsplit=3)
                    print(f"Processing REGUS: nombre={nombre}, email={email}, password={password}, tipo={tipo}")

                    cursor.execute("SELECT id FROM usuarios WHERE email = ?", (email,))
                    if cursor.fetchone() is not None:
                        respuesta = f"El usuario con email {email} ya existe."
                    else:
                        cursor.execute("INSERT INTO usuarios (nombre, email, password, tipo) VALUES (?, ?, ?, ?)", (nombre, email, password, tipo))
                        conn.commit()
                        respuesta = f"Usuario {nombre} ha sido registrado exitosamente."
                        print(f"Insertado en la base de datos: nombre={nombre}, email={email}, password={password}, tipo={tipo}")
                except Exception as e:
                    respuesta = f"Error procesando REGUS: {e}"
                    print(f"Error: {e}")
            else:
                respuesta = "Comando no reconocido."

            # Enviar respuesta
            response_length = len(respuesta)
            message = f"{response_length:05}".encode() + f"regus".encode() + respuesta.encode()
            print('sending {!r}'.format(message))
            sock.sendall(message)

finally:
    print('closing socket')
    conn.close()
    sock.close()

