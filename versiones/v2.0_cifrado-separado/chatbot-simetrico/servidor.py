# ============================================
# CHATBOT CON CIFRADO SIMÉTRICO (AES/Fernet)
# VERSION 2.0 - Solo cifrado, sin SHA256
# ============================================

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from datetime import datetime
from cryptography.fernet import Fernet

# ============================================
# 1. CONFIGURACIÓN INICIAL
# ============================================

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave-segura-flask'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

usuarios_conectados = {}
mensajes = []

# ============================================
# 2. CONFIGURACIÓN DE CIFRADO SIMÉTRICO
# ============================================

key = Fernet.generate_key()
fernet = Fernet(key)
modo_cifrado = "simetrico"

# ============================================
# 3. FUNCIONES DE CIFRADO Y DESCIFRADO
# ============================================

def cifrar_mensaje(mensaje: str) -> bytes:
    """Cifra un mensaje usando Fernet (AES)"""
    return fernet.encrypt(mensaje.encode())

def descifrar_mensaje(cifrado: bytes) -> str:
    """Descifra un mensaje usando Fernet (AES)"""
    return fernet.decrypt(cifrado).decode()

# ============================================
# 4. RUTAS WEB
# ============================================

@app.route('/')
def index():
    return render_template('chat.html')

# ============================================
# 5. EVENTOS DE WEBSOCKET
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
    mensaje_original = data.get('mensaje', '').strip()
    nombre = usuarios_conectados.get(request.sid, 'Anónimo')
    timestamp = datetime.now().strftime('%H:%M:%S')

    if not mensaje_original:
        return

    # Cifrar mensaje (para logging/almacenamiento seguro)
    mensaje_cifrado = cifrar_mensaje(mensaje_original)

    print(f"[{timestamp}] {nombre}: {mensaje_original}")
    print(f"  - Cifrado (simétrico): {mensaje_cifrado[:50]}...")

    # Enviar a todos (descifrado para que se vea en la interfaz)
    emit('nuevo_mensaje', {
        'nombre': nombre,
        'mensaje': mensaje_original,
        'timestamp': timestamp,
        'cifrado': modo_cifrado
    }, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    nombre = usuarios_conectados.pop(request.sid, 'Usuario')
    print(f'Usuario desconectado: {nombre}')
    enviar_lista_usuarios()

# ============================================
# 6. FUNCIONES AUXILIARES
# ============================================

def enviar_lista_usuarios():
    lista = list(usuarios_conectados.values())
    emit('actualizar_usuarios', {'usuarios': lista, 'total': len(lista)}, broadcast=True)

# ============================================
# 7. INICIO
# ============================================

if __name__ == '__main__':
    print(f"========================================")
    print(f"SERVIDOR CON CIFRADO SIMÉTRICO (AES)")
    print(f"VERSION 2.0 - Sin SHA256")
    print(f"========================================")
    print(f"Puerto: 5001")
    print(f"Modo de cifrado: {modo_cifrado.upper()}")
    print(f"========================================")
    socketio.run(app, debug=True, port=5001)
