# ============================================
# CHATBOT BÁSICO - VERSION 1.0
# ============================================
# Chat simple con sockets y UI básica
# Sin cifrado, sin SHA256, sin MD5

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from datetime import datetime

# ============================================
# 1. CONFIGURACIÓN INICIAL
# ============================================

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave-segura-flask'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

usuarios_conectados = {}
mensajes = []

# ============================================
# 2. RUTAS WEB
# ============================================

@app.route('/')
def index():
    return render_template('chat.html')

# ============================================
# 3. EVENTOS DE WEBSOCKET
# ============================================

@socketio.on('connect')
def handle_connect():
    print(f'Nueva conexión: {request.sid}')

@socketio.on('registrar_usuario')
def handle_registrar_usuario(data):
    nombre = data.get('nombre', 'Anónimo').strip() or 'Anónimo'
    usuarios_conectados[request.sid] = nombre

    print(f'Usuario registrado: {nombre}')
    emit('registro_exitoso', {'nombre': nombre})
    enviar_lista_usuarios()

@socketio.on('enviar_mensaje')
def handle_mensaje(data):
    mensaje = data.get('mensaje', '').strip()
    nombre = usuarios_conectados.get(request.sid, 'Anónimo')
    timestamp = datetime.now().strftime('%H:%M:%S')

    if not mensaje:
        return

    print(f"[{timestamp}] {nombre}: {mensaje}")

    # Enviar a todos (sin cifrado)
    emit('nuevo_mensaje', {
        'nombre': nombre,
        'mensaje': mensaje,
        'timestamp': timestamp
    }, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    nombre = usuarios_conectados.pop(request.sid, 'Usuario')
    print(f'Usuario desconectado: {nombre}')
    enviar_lista_usuarios()

# ============================================
# 4. FUNCIONES AUXILIARES
# ============================================

def enviar_lista_usuarios():
    lista = list(usuarios_conectados.values())
    emit('actualizar_usuarios', {'usuarios': lista, 'total': len(lista)}, broadcast=True)

# ============================================
# 5. INICIO
# ============================================

if __name__ == '__main__':
    print(f"========================================")
    print(f"CHATBOT BÁSICO - VERSION 1.0")
    print(f"========================================")
    print(f"Puerto: 5000")
    print(f"Sin cifrado, sin SHA256")
    print(f"========================================")
    socketio.run(app, debug=True, port=5000)
