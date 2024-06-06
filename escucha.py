import socket
import sqlite3

def handle_registration(sock):
    data = sock.recv(50).decode()  # Longitud máxima del mensaje después del header
    print("Datos recibidos:", data)

    # Extraer información del mensaje
    parts = data.split(',')
    name = parts[0].split(':')[1]
    email = parts[1].split(':')[1]
    password = parts[2].split(':')[1]

    # Guardar en la base de datos
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', (name, email, password))
    conn.commit()
    conn.close()
    print("Usuario registrado.")

def listen_for_registrations():
    # Crea un socket TCP/IP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 5000)
    sock.bind(server_address)
    sock.listen(1)

    try:
        print("Esperando mensajes...")
        connection, client_address = sock.accept()
        try:
            handle_registration(connection)
        finally:
            connection.close()
    finally:
        sock.close()

listen_for_registrations()
