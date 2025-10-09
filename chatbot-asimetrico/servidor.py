# ============================================
# CHATBOT CON CIFRADO ASIMÉTRICO (RSA)
# ============================================

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from datetime import datetime
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
import hashlib

# ============================================
# 1. CONFIGURACIÓN INICIAL
# ============================================

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave-segura-flask'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

usuarios_conectados = {}
mensajes = []

# ============================================
# 2. CONFIGURACIÓN DE CIFRADO ASIMÉTRICO
# ============================================

private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()
modo_cifrado = "asimetrico"

# ============================================
# 3. FUNCIONES DE CIFRADO, DESCIFRADO Y HASHING
# ============================================

def cifrar_mensaje(mensaje: str) -> bytes:
    """Cifra un mensaje usando RSA"""
    return public_key.encrypt(
        mensaje.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def descifrar_mensaje(cifrado: bytes) -> str:
    """Descifra un mensaje usando RSA"""
    return private_key.decrypt(
        cifrado,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    ).decode()

def hashear_mensaje(mensaje: str) -> str:
    """Genera un hash SHA256 del mensaje para verificar integridad"""
    return hashlib.sha256(mensaje.encode()).hexdigest()

def verificar_hash(mensaje: str, hash_recibido: str) -> bool:
    """Verifica que el hash del mensaje coincida con el hash recibido"""
    hash_calculado = hashear_mensaje(mensaje)
    return hash_calculado == hash_recibido

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

    # Generar hash para verificar integridad
    mensaje_hash = hashear_mensaje(mensaje_original)

    print(f"[{timestamp}] {nombre}: {mensaje_original}")
    print(f"  - Cifrado (asimétrico): {mensaje_cifrado[:50]}...")
    print(f"  - Hash (SHA256): {mensaje_hash}")

    # Enviar a todos (descifrado para que se vea en la interfaz)
    emit('nuevo_mensaje', {
        'nombre': nombre,
        'mensaje': mensaje_original,  # enviar descifrado
        'hash': mensaje_hash,          # hash para verificar integridad
        'timestamp': timestamp,
        'cifrado': modo_cifrado
    }, broadcast=True)

@socketio.on('mensaje_descifrar')
def handle_descifrar(data):
    """Permite a un cliente pedir descifrado (opcional, para debug)"""
    cifrado = data.get('mensaje', '').encode('latin1')
    mensaje_descifrado = descifrar_mensaje(cifrado)
    emit('mensaje_descifrado', {'mensaje': mensaje_descifrado})

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
    print(f"SERVIDOR CON CIFRADO ASIMÉTRICO (RSA)")
    print(f"========================================")
    print(f"Puerto: 5002")
    print(f"Modo de cifrado: {modo_cifrado.upper()}")
    print(f"========================================")
    socketio.run(app, debug=True, port=5002)
