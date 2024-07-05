import socket
import sys

# Función para enviar mensajes al servidor y recibir respuestas
def enviar_mensaje(sock, mensaje):
    try:
        sock.sendall(mensaje)
        header = sock.recv(5)
        if not header:
            return "No response from server."
        amount_expected = int(header)

        data = b""
        while len(data) < amount_expected:
            chunk = sock.recv(amount_expected - len(data))
            if not chunk:
                break
            data += chunk

        return data.decode()
    except Exception as e:
        return f"Error during communication: {e}"

# Crear un socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar el socket al puerto donde el bus está escuchando
bus_address = ('localhost', 5001)
print('connecting to {} port {}'.format(*bus_address))
sock.connect(bus_address)

try:
    while True:
        opcion = input("Choose an option: [1] Register, [2] Login, [3] Exit: ")
        if opcion == '1':
            nombre = input('Enter name: ')
            email = input('Enter email: ')
            password = input('Enter password: ')
            tipo = input('Is this a lawyer or a client? (lawyer/client): ')
            datos = f"{nombre} {email} {password} {tipo}"
            mensaje = f"{len(datos) + 5:05}regus".encode() + datos.encode()
            respuesta = enviar_mensaje(sock, mensaje)
            print('Response:', respuesta)
        elif opcion == '2':
            email = input('Enter email: ')
            password = input('Enter password: ')
            datos = f"{email} {password}"
            mensaje = f"{len(datos) + 5:05}login".encode() + datos.encode()
            respuesta = enviar_mensaje(sock, mensaje)
            print('Response:', respuesta)

            if "Login exitoso" in respuesta:
                user_id, user_tipo = respuesta.split("ID: ")[1].split(", Tipo: ")
                user_id = user_id.strip()
                user_tipo = user_tipo.strip()

                if user_tipo == "client":
                    while True:
                        opcion_client = input("Choose an option: [1] Upload Case, [2] Logout: ")
                        if opcion_client == '1':
                            descripcion = input('Enter case description: ')
                            datos = f"{user_id} {descripcion}"
                            mensaje = f"{len(datos) + 5:05}upcas".encode() + datos.encode()
                            respuesta = enviar_mensaje(sock, mensaje)
                            print('Response:', respuesta)
                        elif opcion_client == '2':
                            break

                elif user_tipo == "lawyer":
                    while True:
                        opcion_lawyer = input("Choose an option: [1] View Cases, [2] Take Case, [3] Logout: ")
                        if opcion_lawyer == '1':
                            cursor.execute("SELECT id, descripcion FROM casos WHERE estado = 'disponible'")
                            casos = cursor.fetchall()
                            if casos:
                                print("Available cases:")
                                for caso in casos:
                                    print(f"Case ID: {caso[0]}, Description: {caso[1]}")
                            else:
                                print("No available cases.")
                        elif opcion_lawyer == '2':
                            caso_id = input('Enter case ID to take: ')
                            datos = f"{user_id} {caso_id}"
                            mensaje = f"{len(datos) + 5:05}tkcas".encode() + datos.encode()
                            respuesta = enviar_mensaje(sock, mensaje)
                            print('Response:', respuesta)
                        elif opcion_lawyer == '3':
                            break
        elif opcion == '3':
            break

finally:
    print('closing socket')
    sock.close()

