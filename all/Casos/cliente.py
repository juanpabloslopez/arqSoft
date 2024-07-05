import socket
import sys

def validar_entrada(entrada, tipo):
    if tipo == "int":
        try:
            return int(entrada)
        except ValueError:
            return None
    elif tipo == "usuario":
        if entrada.strip() == "":
            return None
        return entrada
    elif tipo == "descripcion" or tipo == "etiqueta":
        return entrada

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
        case_id = validar_entrada(case_id, "int")
        if case_id is None:
            print("Invalid ID. Must be an integer.")
            continue

        etiqueta = input('Enter case label: ')
        etiqueta = validar_entrada(etiqueta, "etiqueta")

        usuario = input('Enter user: ')
        usuario = validar_entrada(usuario, "usuario")
        if usuario is None:
            print("Invalid user. Must not be empty.")
            continue

        descripcion = input('Enter case description: ')
        descripcion = validar_entrada(descripcion, "descripcion")

        datos = f"{case_id}|{etiqueta}|{usuario}|{descripcion}|No asignado"
        mensaje = f"{len(datos) :05}subcs".encode() + datos.encode()
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
