import socket
import sys

# Crear un socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar el socket al puerto donde el bus está escuchando
bus_address = ('localhost', 5000)
print('connecting to {} port {}'.format(*bus_address))
sock.connect(bus_address)

try:
    while True:
        # Enviar mensaje de registro de usuario al servicio
        if input('Register user? y/n: ') != 'y':
            break
        nombre = input('Enter name: ')
        email = input('Enter email: ')
        password = input('Enter password: ')
        tipo = input('Is this a lawyer or a client? (lawyer/client): ')
        datos = f"{nombre} {email} {password} {tipo}"
        mensaje = f"{len(datos) + 5:05}regus".encode() + datos.encode()
        print('sending {!r}'.format(mensaje))
        sock.sendall(mensaje)

        # Esperar la respuesta
        print("Waiting for transaction")
        amount_received = 0
        amount_expected = int(sock.recv(5))

        data = b""
        while amount_received < amount_expected:
            chunk = sock.recv(amount_expected - amount_received)
            amount_received += len(chunk)
            data += chunk
        print("Checking server answer ...")
        print('received {!r}'.format(data))

finally:
    print('closing socket')
    sock.close()

