import socket

def register_user():
    # Crea un socket TCP/IP
    sock = socket.socket(socket.AF_COM_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 5000)
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
        response_length = int(sock.recv(5).decode())
        response = sock.recv(response_only_length).decode()
        print("Respuesta recibida:", response)

    finally:
        sock.close()

register_user()
