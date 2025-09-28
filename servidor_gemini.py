from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from datetime import datetime
import google.generativeai as genai
from config import GEMINI_API_KEY, AGENTE_CONFIG

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu-clave-secreta-aqui'
socketio = SocketIO(app, cors_allowed_origins="*")

# Configurar Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash-exp')

# Historial de conversación para mantener contexto
conversacion_historial = {}

def obtener_respuesta_gemini(mensaje, session_id):
    """Obtiene respuesta de Gemini con el contexto del agente especializado"""
    try:
        # Obtener o crear historial para esta sesión
        if session_id not in conversacion_historial:
            conversacion_historial[session_id] = []

        # Crear prompt con contexto del agente
        prompt_sistema = f"""
        {AGENTE_CONFIG['instrucciones_especiales']}

        Tu nombre es: {AGENTE_CONFIG['nombre']}
        Especialidad: {AGENTE_CONFIG['rubro']}
        Personalidad: {AGENTE_CONFIG['personalidad']}

        Historial de conversación:
        {' '.join(conversacion_historial[session_id][-5:])}  # Últimos 5 mensajes

        Usuario: {mensaje}

        Responde de manera concisa y útil:
        """

        # Generar respuesta
        response = model.generate_content(prompt_sistema)
        respuesta = response.text

        # Guardar en historial
        conversacion_historial[session_id].append(f"Usuario: {mensaje}")
        conversacion_historial[session_id].append(f"Bot: {respuesta}")

        # Limitar historial a 20 mensajes
        if len(conversacion_historial[session_id]) > 20:
            conversacion_historial[session_id] = conversacion_historial[session_id][-20:]

        return respuesta

    except Exception as e:
        print(f"Error al conectar con Gemini: {e}")
        return f"Lo siento, tuve un problema al procesar tu mensaje. Error: {str(e)}"

@app.route('/')
def index():
    """Ruta principal que sirve la interfaz HTML"""
    return render_template('chat_bot.html')

@socketio.on('connect')
def handle_connect():
    """Maneja nuevas conexiones"""
    print(f'Cliente conectado: {request.sid}')

    # Mensaje de bienvenida personalizado
    mensaje_bienvenida = f"""⚖️ ¡Bienvenido a {AGENTE_CONFIG['nombre']}!

Soy tu consultor legal especializado en {AGENTE_CONFIG['rubro']}.

✅ Puedo ayudarte con:
• Consultas sobre Código Civil y Mercantil
• Derecho Laboral y Seguridad Social
• Procedimientos legales y trámites
• Jurisprudencia de la SCJN
• Orientación en derecho fiscal

⚠️ IMPORTANTE: Mis respuestas son orientativas. Para casos específicos, siempre consulta con un abogado colegiado.

¿En qué consulta legal puedo asistirte hoy?"""

    emit('mensaje_bot', {
        'texto': mensaje_bienvenida,
        'timestamp': datetime.now().strftime('%H:%M:%S')
    })

@socketio.on('disconnect')
def handle_disconnect():
    """Maneja desconexiones y limpia el historial"""
    print(f'Cliente desconectado: {request.sid}')
    # Limpiar historial de esta sesión
    if request.sid in conversacion_historial:
        del conversacion_historial[request.sid]

@socketio.on('enviar_mensaje')
def handle_mensaje(data):
    """Recibe mensaje del cliente y responde con Gemini"""
    mensaje = data.get('mensaje', '')
    timestamp = datetime.now().strftime('%H:%M:%S')

    if mensaje:
        print(f"[{timestamp}] Cliente {request.sid[:8]}: {mensaje}")

        # Enviar confirmación de mensaje recibido a todos
        emit('nuevo_mensaje', {
            'cliente_id': request.sid[:8],
            'mensaje': mensaje,
            'timestamp': timestamp,
            'es_usuario': True
        }, broadcast=True)

        # Obtener respuesta de Gemini
        emit('bot_escribiendo', {'estado': True})  # Mostrar que el bot está escribiendo

        respuesta_bot = obtener_respuesta_gemini(mensaje, request.sid)

        # Enviar respuesta del bot
        emit('mensaje_bot', {
            'texto': respuesta_bot,
            'timestamp': datetime.now().strftime('%H:%M:%S')
        }, broadcast=True)

        emit('bot_escribiendo', {'estado': False})  # Ocultar indicador de escritura

@socketio.on('limpiar_chat')
def handle_limpiar():
    """Limpia el historial de conversación"""
    if request.sid in conversacion_historial:
        conversacion_historial[request.sid] = []
    emit('chat_limpiado', {})

if __name__ == '__main__':
    print(f"""
    ========================================
    SERVIDOR CHATBOT CON GEMINI INICIADO
    ========================================
    Agente: {AGENTE_CONFIG['nombre']}
    Especialidad: {AGENTE_CONFIG['rubro']}
    URL: http://localhost:5001
    ========================================
    """)
    socketio.run(app, debug=True, port=5001)