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
        # Enviar mensaje de caso al servicio
        if input('Send case to servi? y/n: ') != 'y':
            break
        case_id = input('Enter case ID: ')
        descripcion = input('Enter case description: ')
        datos = f"{case_id} {descripcion}"
        mensaje = f"{len(datos) + 5:05}subcs".encode() + datos.encode()
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
        print("Checking servi answer ...")
        print('received {!r}'.format(data))

finally:
    print('closing socket')
    sock.close()
