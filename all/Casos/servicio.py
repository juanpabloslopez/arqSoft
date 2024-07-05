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
conn = sqlite3.connect('casos.db')
cursor = conn.cursor()

# Crear la tabla de casos si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS casos (
        id INTEGER PRIMARY KEY,
        etiqueta TEXT NOT NULL,
        usuario TEXT NOT NULL,
        descripcion TEXT NOT NULL,
        abogado TEXT DEFAULT 'No asignado'
    )
''')
conn.commit()

try:
    # Enviar datos de inicio
    message = b'00010sinitsubcs'
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
            datos = data[5:].decode()  # Asegúrate de decodificar los datos
            if comando == "subcs":
                try:
                    case_id, etiqueta, usuario, descripcion, abogado = datos.split('|', 4)
                    case_id = int(case_id)
                    print(f"Processing SUBCS: case_id={case_id}, etiqueta={etiqueta}, usuario={usuario}, descripcion={descripcion}, abogado={abogado}")

                    cursor.execute("SELECT id FROM casos WHERE id = ?", (case_id,))
                    if cursor.fetchone() is not None:
                        respuesta = f"El caso {case_id} ya existe."
                    else:
                        cursor.execute("INSERT INTO casos (id, etiqueta, usuario, descripcion, abogado) VALUES (?, ?, ?, ?, ?)", (case_id, etiqueta, usuario, descripcion, abogado))
                        conn.commit()
                        respuesta = f"El caso {case_id} ha sido subido exitosamente."
                        print(f"Insertado en la base de datos: case_id={case_id}, etiqueta={etiqueta}, usuario={usuario}, descripcion={descripcion}, abogado={abogado}")
                except Exception as e:
                    respuesta = f"Error procesando SUBCS: {e}"
                    print(f"Error: {e}")
            else:
                respuesta = "Comando no reconocido."

            # Enviar respuesta
            response_length = len(respuesta) + 5 + 5  # Longitud del comando y longitud del encabezado
            message = f"{response_length:05}".encode() + b"subcs" + respuesta.encode()  # Asegúrate de que todo sea bytes
            print('sending {!r}'.format(message))
            sock.sendall(message)

finally:
    print('closing socket')
    conn.close()
    sock.close()
