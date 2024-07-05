from flask import Flask, render_template, redirect, url_for, request
import socket

app = Flask(__name__)

# Crear un socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar el socket al puerto donde el bus está escuchando
bus_address = ('localhost', 5000)
sock.connect(bus_address)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        datos = f"{email}|{password}"
        mensaje = f"{len(datos) + 10:05}auth1logus".encode() + datos.encode()
        sock.sendall(mensaje)

        amount_received = 0
        amount_expected = int(sock.recv(5))

        data = b""
        while amount_received < amount_expected:
            chunk = sock.recv(amount_expected - amount_received)
            amount_received += len(chunk)
            data += chunk

        if data.startswith(b'auth1OKOK1') or data.startswith(b'auth1OKOK2'):
            user_info = data[8:].decode().split(';')
            if len(user_info) == 3:
                user_id, nombre = user_info[1], user_info[2]
                tipo_usuario = 1 if data.startswith(b'auth1OKOK1') else 2
                return redirect(url_for('perfil', tipo_usuario=tipo_usuario, user_id=user_id, nombre=nombre))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        lawyer_key = request.form['lawyer_key']
        datos = f"{username}|{email}|{password}|{lawyer_key}"
        mensaje = f"{len(datos) + 10:05}auth1regus".encode() + datos.encode()
        sock.sendall(mensaje)

        amount_received = 0
        amount_expected = int(sock.recv(5))

        data = b""
        while amount_received < amount_expected:
            chunk = sock.recv(amount_expected - amount_received)
            amount_received += len(chunk)
            data += chunk

        if data.startswith(b'auth1OKOK1') or data.startswith(b'auth1OKOK2'):
            user_info = data[8:].decode().split(';')
            if len(user_info) == 3:
                user_id, nombre = user_info[1], user_info[2]
                tipo_usuario = 1 if data.startswith(b'auth1OKOK1') else 2
                return redirect(url_for('perfil', tipo_usuario=tipo_usuario, user_id=user_id, nombre=nombre))

    return render_template('register.html')

@app.route('/perfil/<int:tipo_usuario>/<int:user_id>/<string:nombre>')
def perfil(tipo_usuario, user_id, nombre):
    print(f"Perfil - tipo_usuario: {tipo_usuario}, user_id: {user_id}, nombre: {nombre}")  # Agregar print para verificar los valores
    if tipo_usuario == 1:
        return render_template('perfil.html', tipo_usuario=tipo_usuario, user_id=user_id, nombre=nombre)
    elif tipo_usuario == 2:
        casos = obtener_casos_abogado()
        return render_template('perfil.html', tipo_usuario=tipo_usuario, user_id=user_id, nombre=nombre, casos=casos)


@app.route('/subir_caso', methods=['POST'])
def subir_caso():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        tipo_usuario = request.form.get('tipo_usuario', 1)  # Valor predeterminado de 1
        nombre = request.form.get('nombre')

        print(f"user_id: {user_id}, tipo_usuario: {tipo_usuario}, nombre: {nombre}")  # Verificar los valores

        try:
            user_id = int(user_id)
            tipo_usuario = int(tipo_usuario)

            etiqueta = request.form['etiqueta']
            descripcion = request.form['descripcion']

            datos = f"{etiqueta}|{nombre}|{descripcion}|No asignado|{user_id}"
            mensaje = f"{len(datos):05}subcscliente".encode() + datos.encode()
            sock.sendall(mensaje)

            amount_received = 0
            amount_expected = int(sock.recv(5))

            data = b""
            while amount_received < amount_expected:
                chunk = sock.recv(amount_expected - amount_received)
                amount_received += len(chunk)
                data += chunk

            if data.startswith(b'subcsclienteEl caso'):
                return render_template('perfil.html', user_id=user_id, tipo_usuario=tipo_usuario, nombre=nombre, success="El caso se ha subido correctamente.")
            else:
                return render_template('perfil.html', user_id=user_id, tipo_usuario=tipo_usuario, nombre=nombre, success="El caso se ha subido correctamente.")

        except KeyError as e:
            return render_template('perfil.html', user_id=user_id, tipo_usuario=tipo_usuario, nombre=nombre, error=f"Falta el campo {e}")
        except Exception as e:
            return render_template('perfil.html', user_id=user_id, tipo_usuario=tipo_usuario, nombre=nombre, error=f"Error: {e}")

    return render_template('perfil.html', user_id=user_id, tipo_usuario=tipo_usuario, nombre=nombre)


def obtener_casos_abogado():
    datos = "Solicitando lista de casos"
    mensaje = f"{len(datos):05}subcsabogado".encode() + datos.encode()
    sock.sendall(mensaje)
    amount_received = 0
    amount_expected = int(sock.recv(5))
    data = b""
    while amount_received < amount_expected:
        chunk = sock.recv(amount_expected - amount_received)
        amount_received += len(chunk)
        data += chunk

    casos_json = []
    casos_raw = data[14:].decode().strip()
    casos_list = casos_raw.split('\n')

    for caso_raw in casos_list:
        if caso_raw.strip():
            caso_info = caso_raw.split(', ')
            caso_json = {}
            for info in caso_info:
                key_value = info.split(': ')
                if len(key_value) == 2:
                    caso_json[key_value[0].strip()] = key_value[1].strip()
            if 'ID' not in caso_json:
                caso_json['ID'] = None
            casos_json.append(caso_json)

    return casos_json
    return render_template('chat.html', tipo_usuario=tipo_usuario, user_id=user_id, caso_id=caso_id, nombre_usuario=nombre_usuario, historial_chat=historial)


@app.route('/chat/<int:tipo_usuario>/<int:user_id>/<int:caso_id>/<string:nombre_usuario>/<int:receiver_id>', methods=['GET', 'POST'])
def chat(tipo_usuario, user_id, caso_id, nombre_usuario, receiver_id):
    if request.method == 'POST':
        mensaje = request.form['mensaje']
        sender_id = user_id  # ID del usuario que envía el mensaje
        service_name = 'msjes'
        formatted_message = f'{len(service_name + "envi:" + str(sender_id) + ":" + str(receiver_id) + ":" + mensaje):05d}{service_name}envi:{sender_id}:{receiver_id}:{mensaje}'.encode()
        sock.sendall(formatted_message)
        amount_received = 0
        amount_expected = int(sock.recv(5))
        data = b""
        while amount_received < amount_expected:
            chunk = sock.recv(amount_expected - amount_received)
            amount_received += len(chunk)
            data += chunk
        if data.decode() == 'msjesOKenviOK':
            print("Mensaje enviado correctamente")
    
    historial = historial_chat(user_id, receiver_id)  # Usar ambos ID de usuario para el historial
    return render_template('chat.html', tipo_usuario=tipo_usuario, user_id=user_id, caso_id=caso_id, nombre_usuario=nombre_usuario, historial_chat=historial, receiver_id=receiver_id)

    
def historial_chat(sender_id, receiver_id):
    try:
        service_name = 'msjeschat'
        formatted_request = f'{len(service_name + ":" + str(sender_id) + ":" + str(receiver_id)):05d}{service_name}:{sender_id}:{receiver_id}'.encode()
        sock.sendall(formatted_request)
        amount_received = 0
        amount_expected = int(sock.recv(5))
        chat_data = b''
        while amount_received < amount_expected:
            chunk = sock.recv(amount_expected - amount_received)
            if not chunk:
                break
            chat_data += chunk
            amount_received += len(chunk)

        chat_history = []
        if chat_data:
            chat_lines = chat_data.decode().split('\n')
            for line in chat_lines:
                if line.strip():
                    parts = line.split(', ')
                    if len(parts) == 3:
                        sender, receiver, message = parts
                        chat_history.append({'sender': sender.split(': ')[1], 'receiver': receiver.split(': ')[1], 'message': message.split(': ')[1]})

        return chat_history

    except Exception as e:
        print(f"Error al obtener historial de chat: {e}")
        return []

    except Exception as e:
        print(f"Error al obtener historial de chat: {e}")
        return []

if __name__ == '__main__':
    app.run(debug=True, port=8080)
