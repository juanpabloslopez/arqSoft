import socket
import sys

def send_message(sock, service_name, data):
    full_message = f"{len(service_name + data):05d}{service_name}{data}".encode('utf-8')
    sock.sendall(full-one_message)

def receive_message(sock):
    # Leer la longitud del mensaje
    length = int(sock.recv(5))
    # Leer el mensaje completo
    message = sock.recv(length).decode('utf-8')
    return message

# Establecer conexión con el bus
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bus_address = ('localhost', 5000)
sock.connect(bus_address)

try:
    while True:
        user_input = input("Do you want to register (1) or authenticate (2)? Press 'q' to quit: ")
        if user_input == 'q':
            break
        elif user_input == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            email = input("Enter email: ")
            send_message(sock, 'regist', f"{username}{password}{email}")
        elif user_input == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            send_message(sock, 'authen', f"{username}{password}")

# Esperar respuesta del servicio
        print("Waiting for service response...")
        response = receive_message(sock)
        print("Service response:", response)

finally:
    print('Closing socket')
    sock.close()
