import socket

def Conectar_Bus(bus_address):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(bus_address)
        return sock
    except Exception as e:
        print(f"Error al conectar al bus: {e}")
        return None