from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu-clave-secreta-aqui'
socketio = SocketIO(app, cors_allowed_origins="*")

# Lista para almacenar mensajes
mensajes = []

@app.route('/')
def index():
    """Ruta principal que sirve la interfaz HTML"""
    return render_template('chat.html')

@socketio.on('connect')
def handle_connect():
    """Maneja nuevas conexiones"""
    print(f'Cliente conectado: {request.sid}')
    emit('mensaje_servidor', {
        'texto': 'Bienvenido al chat!',
        'timestamp': datetime.now().strftime('%H:%M:%S')
    })

@socketio.on('disconnect')
def handle_disconnect():
    """Maneja desconexiones"""
    print(f'Cliente desconectado: {request.sid}')

@socketio.on('enviar_mensaje')
def handle_mensaje(data):
    """Recibe mensaje del cliente y lo retransmite"""
    mensaje = data.get('mensaje', '')
    timestamp = datetime.now().strftime('%H:%M:%S')

    if mensaje:
        # Guardar mensaje
        mensajes.append({
            'cliente_id': request.sid[:8],
            'mensaje': mensaje,
            'timestamp': timestamp
        })

        print(f"[{timestamp}] Cliente {request.sid[:8]}: {mensaje}")

        # Enviar mensaje a todos los clientes conectados
        emit('nuevo_mensaje', {
            'cliente_id': request.sid[:8],
            'mensaje': mensaje,
            'timestamp': timestamp
        }, broadcast=True)

        # Respuesta del servidor
        if mensaje.lower() != 'salir':
            emit('mensaje_servidor', {
                'texto': f'Servidor recibió: {mensaje}',
                'timestamp': datetime.now().strftime('%H:%M:%S')
            })

if __name__ == '__main__':
    print("Servidor web iniciado en http://localhost:5000")
    socketio.run(app, debug=True, port=5000)