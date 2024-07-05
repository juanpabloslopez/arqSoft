import socket

# Crear un socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar el socket al puerto donde el bus está escuchando
bus_address = ('localhost', 5000)
print('Conectando a {} puerto {}'.format(*bus_address))
sock.connect(bus_address)

try:
    # Enviar datos
    message = b'00010sinitmsjes'
    print('Enviando {!r}'.format(message))
    sock.sendall(message)
    sinit = 1

    mensajes_recibidos = []  # Lista para almacenar los mensajes

    while True:
        # Esperar la respuesta
        print("Esperando transacción")
        amount_received = 0
        amount_expected = int(sock.recv(5))
        data = b''
        while amount_received < amount_expected:
            chunk = sock.recv(amount_expected - amount_received)
            data += chunk
            amount_received += len(chunk)

        service_name = data[:5].decode()  # Extraer el nombre del servicio

        # Verificar si el mensaje proviene del cliente antes de dividirlo
        if service_name == 'msjes':
            mensaje = data[5:].decode()  # Extraer solo el mensaje sin el nombre del servicio
            username, mensaje = mensaje.split(':', 1)  # Separar nombre de usuario y mensaje usando ':'

            print("Procesando...")
            print('Recibido mensaje de {!r}'.format(username))
            print('Nombre del servicio:', service_name)
            print('Mensaje:', mensaje)

            mensajes_recibidos.append(f"{username}: {mensaje}")  # Agregar el mensaje completo con el nombre de usuario

        if sinit == 1:
            sinit = 0
            print('Respuesta de inicialización recibida')
        else:
            print("Enviando respuesta")
            message = b'00013msjesReceived'
            print('Enviando {!r}'.format(message))
            sock.sendall(message)

        # Imprimir todos los mensajes recibidos hasta el momento, con los nombres de usuario, separados por un salto de línea
        print("\n".join(mensajes_recibidos))

finally:
    print('Cerrando el socket')
    sock.close()