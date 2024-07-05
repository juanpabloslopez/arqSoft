import socket

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the bus is listening
bus_address = ('localhost', 5000)
print('connecting to {} port {}'.format(*bus_address))
sock.connect(bus_address)

try:
    username = input('Enter your username: ')

    while True:
        # Solicitar al usuario que ingrese un mensaje para enviar al servicio
        if input('Send a message to servi? (y/n): ') != 'y':
            break
        # El usuario ingresa el mensaje que desea enviar
        custom_message = input('Enter your message: ')
        # Preparar el mensaje, asegurándose de que el tamaño total (NNNNN) y el mensaje se codifiquen correctamente
        # Asumiendo que el mensaje siempre debe ser enviado al servicio "corvi"
        service_name = 'msjes'
        formatted_message = f'{len(service_name + username + custom_message):05d}{service_name}{username}:{custom_message}'  # Incluir ':' como delimitador
        message = formatted_message.encode()
        print('sending {!r}'.format(message))
        sock.sendall(message)

        # Look for the response
        print("Waiting for transaction")
        amount_received = 0
        amount_expected = int(sock.recv(5))  # Aquí estamos asumiendo que el bus siempre envía la longitud primero

        data = b''
        while amount_received < amount_expected:
            chunk = sock.recv(amount_expected - amount_received)
            if not chunk:
                break  # Socket connection might be broken
            data += chunk
            amount_received += len(chunk)
        
        print("Checking servi answer ...")
        print('received {!r}'.format(data))

finally:
    print('closing socket')
    sock.close()