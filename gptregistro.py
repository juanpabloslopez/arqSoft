import socket
import sys

def register_user():
    # Crea un socket TCP/IP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 5100)
    sock.connect(server_address)

    try:
        # Solicitar información del usuario
        name = input("Ingrese su nombre: ")
        email = input("Ingrese su email: ")
        password = input("Ingrese su contraseña: ")

        # Crear el mensaje según el formato del bus
        data = f"nombre:{name},email:{email},pass:{password}"
        message = f"{len(data):05}regus{data}"
        print(f"Enviando: {message}")

        # Enviar el mensaje
        sock.sendall(message.encode())

        # Esperar la respuesta
        raw_length = sock.recv(5).decode()
        if not raw_length:
            print("No se recibió respuesta del servidor.")
            return

        response_length = int(raw_length)
        response = sock.recv(response_length).decode()  # Asegurarse de leer la cantidad de bytes esperada
        print("Respuesta recibida:", response)

    finally:
        sock.close()

register_user()
