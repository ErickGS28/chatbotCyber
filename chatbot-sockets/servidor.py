# ============================================
# CHATBOT SIMPLE CON WEBSOCKETS - MÚLTIPLES USUARIOS
# ============================================
# Este es un servidor de chat que retransmite mensajes
# entre múltiples usuarios conectados. No usa inteligencia artificial.

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from datetime import datetime

# ============================================
# 1. CONFIGURACIÓN INICIAL
# ============================================

# Crear la aplicación Flask (el servidor web)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu-clave-secreta-aqui'  # Clave para seguridad

# Crear conexión de WebSocket (para comunicación en tiempo real)
socketio = SocketIO(app, cors_allowed_origins="*")

# Diccionario para guardar usuarios conectados: {session_id: nombre}
usuarios_conectados = {}

# Lista para almacenar mensajes (opcional, para histórico)
mensajes = []

# ============================================
# 2. RUTAS WEB (URLs del servidor)
# ============================================

@app.route('/')
def index():
    """
    Ruta principal: cuando alguien visita http://localhost:5000
    se muestra la página HTML del chat
    """
    return render_template('chat.html')

# ============================================
# 3. EVENTOS DE WEBSOCKET (Comunicación en tiempo real)
# ============================================

@socketio.on('connect')
def handle_connect():
    """
    Se ejecuta cuando un nuevo usuario se conecta al chat
    (todavía no tiene nombre asignado)
    """
    print(f'Nueva conexión: {request.sid}')

@socketio.on('registrar_usuario')
def handle_registrar_usuario(data):
    """
    Se ejecuta cuando el usuario envía su nombre
    1. Guarda el nombre del usuario
    2. Actualiza la lista de usuarios conectados
    3. Notifica a todos que alguien se unió
    """
    nombre = data.get('nombre', 'Anónimo').strip()

    # Si no envió nombre o está vacío, asignar "Anónimo"
    if not nombre:
        nombre = 'Anónimo'

    # Guardar el usuario en el diccionario
    usuarios_conectados[request.sid] = nombre

    print(f'Usuario registrado: {nombre} (ID: {request.sid[:8]})')

    # Enviar confirmación al usuario que se registró
    emit('registro_exitoso', {
        'nombre': nombre,
        'timestamp': datetime.now().strftime('%H:%M:%S')
    })

    # Notificar a TODOS que alguien se unió
    emit('usuario_conectado', {
        'nombre': nombre,
        'timestamp': datetime.now().strftime('%H:%M:%S')
    }, broadcast=True)

    # Enviar lista actualizada de usuarios a TODOS
    enviar_lista_usuarios()

@socketio.on('disconnect')
def handle_disconnect():
    """
    Se ejecuta cuando un usuario se desconecta del chat
    1. Notifica a todos que alguien se fue
    2. Elimina al usuario de la lista
    3. Actualiza la lista de usuarios conectados
    """
    # Obtener el nombre del usuario que se desconectó
    nombre = usuarios_conectados.get(request.sid, 'Usuario')

    print(f'Usuario desconectado: {nombre} (ID: {request.sid[:8]})')

    # Eliminar al usuario del diccionario
    if request.sid in usuarios_conectados:
        del usuarios_conectados[request.sid]

    # Notificar a TODOS que alguien se desconectó
    emit('usuario_desconectado', {
        'nombre': nombre,
        'timestamp': datetime.now().strftime('%H:%M:%S')
    }, broadcast=True)

    # Enviar lista actualizada de usuarios a TODOS
    enviar_lista_usuarios()

@socketio.on('enviar_mensaje')
def handle_mensaje(data):
    """
    Se ejecuta cuando un usuario envía un mensaje
    1. Recibe el mensaje
    2. Obtiene el nombre del usuario
    3. Lo retransmite a TODOS los usuarios conectados
    """
    mensaje = data.get('mensaje', '').strip()

    # Obtener el nombre del usuario que envió el mensaje
    nombre = usuarios_conectados.get(request.sid, 'Anónimo')
    timestamp = datetime.now().strftime('%H:%M:%S')

    if mensaje:
        # Guardar el mensaje en la lista (opcional)
        mensajes.append({
            'nombre': nombre,
            'mensaje': mensaje,
            'timestamp': timestamp
        })

        # Mostrar en la consola del servidor
        print(f"[{timestamp}] {nombre}: {mensaje}")

        # Enviar el mensaje a TODOS los clientes conectados (broadcast=True)
        emit('nuevo_mensaje', {
            'nombre': nombre,
            'mensaje': mensaje,
            'timestamp': timestamp,
            'es_propio': False  # Se actualizará en el cliente
        }, broadcast=True, include_self=False)

        # Enviar confirmación al que envió (para que vea su propio mensaje)
        emit('nuevo_mensaje', {
            'nombre': nombre,
            'mensaje': mensaje,
            'timestamp': timestamp,
            'es_propio': True
        })

@socketio.on('solicitar_usuarios')
def handle_solicitar_usuarios():
    """
    Se ejecuta cuando un cliente solicita la lista de usuarios conectados
    """
    enviar_lista_usuarios()

# ============================================
# 4. FUNCIONES AUXILIARES
# ============================================

def enviar_lista_usuarios():
    """
    Envía la lista actualizada de usuarios conectados a TODOS los clientes
    """
    lista_usuarios = list(usuarios_conectados.values())
    emit('actualizar_usuarios', {
        'usuarios': lista_usuarios,
        'total': len(lista_usuarios)
    }, broadcast=True)

# ============================================
# 5. INICIAR EL SERVIDOR
# ============================================

if __name__ == '__main__':
    # Mostrar información de inicio
    print("""
    ========================================
    💬 CHATBOT MULTIUSUARIO INICIADO
    ========================================
    URL: http://localhost:5000
    ========================================
    Este es un chat que soporta múltiples
    usuarios conectados simultáneamente.

    Características:
    ✅ Múltiples usuarios con nombres
    ✅ Lista de usuarios en tiempo real
    ✅ Notificaciones de entrada/salida
    ✅ Mensajes identificados por nombre

    Presiona Ctrl+C para detener el servidor
    """)

    # Iniciar el servidor en el puerto 5000
    socketio.run(app, debug=True, port=5000)
