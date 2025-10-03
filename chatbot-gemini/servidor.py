# ============================================
# CHATBOT CON INTELIGENCIA ARTIFICIAL (GEMINI)
# ============================================
# Este servidor crea un chatbot web que usa la API de Google Gemini
# para responder de manera inteligente a las preguntas del usuario.

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from datetime import datetime
import google.generativeai as genai
from config import GEMINI_API_KEY, AGENTE_CONFIG

# ============================================
# 1. CONFIGURACIÓN INICIAL
# ============================================

# Crear la aplicación Flask (el servidor web)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu-clave-secreta-aqui'  # Clave para seguridad

# Crear conexión de WebSocket (para comunicación en tiempo real)
socketio = SocketIO(app, cors_allowed_origins="*")

# Configurar la API de Gemini con nuestra clave
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash-exp')  # Modelo de IA a usar

# Diccionario para guardar el historial de cada usuario
# Cada usuario (identificado por session_id) tendrá su propia conversación
conversacion_historial = {}

# ============================================
# 2. FUNCIÓN PRINCIPAL: OBTENER RESPUESTA DE IA
# ============================================

def obtener_respuesta_gemini(mensaje, session_id):
    """
    Esta función envía el mensaje del usuario a Gemini y obtiene una respuesta.

    Parámetros:
    - mensaje: Lo que escribió el usuario
    - session_id: Identificador único del usuario (para mantener su historial)

    Retorna:
    - La respuesta generada por la IA
    """
    try:
        # Si es la primera vez que este usuario habla, crear su historial vacío
        if session_id not in conversacion_historial:
            conversacion_historial[session_id] = []

        # Crear el prompt (instrucciones) para la IA
        # Incluye: quién es el bot, su especialidad, el historial y el mensaje actual
        prompt_sistema = f"""
        {AGENTE_CONFIG['instrucciones_especiales']}

        Tu nombre es: {AGENTE_CONFIG['nombre']}
        Especialidad: {AGENTE_CONFIG['rubro']}
        Personalidad: {AGENTE_CONFIG['personalidad']}

        Historial de conversación:
        {' '.join(conversacion_historial[session_id][-5:])}

        Usuario: {mensaje}

        Responde de manera concisa y útil:
        """

        # Enviar el prompt a Gemini y obtener la respuesta
        response = model.generate_content(prompt_sistema)
        respuesta = response.text

        # Guardar este intercambio en el historial del usuario
        conversacion_historial[session_id].append(f"Usuario: {mensaje}")
        conversacion_historial[session_id].append(f"Bot: {respuesta}")

        # Mantener solo los últimos 20 mensajes para no sobrecargar la memoria
        if len(conversacion_historial[session_id]) > 20:
            conversacion_historial[session_id] = conversacion_historial[session_id][-20:]

        return respuesta

    except Exception as e:
        # Si algo sale mal, mostrar un mensaje de error amigable
        print(f"Error al conectar con Gemini: {e}")
        return f"Lo siento, tuve un problema al procesar tu mensaje. Error: {str(e)}"

# ============================================
# 3. RUTAS WEB (URLs del servidor)
# ============================================

@app.route('/')
def index():
    """
    Ruta principal: cuando alguien visita http://localhost:5001
    se muestra la página HTML del chat
    """
    return render_template('chat.html')

# ============================================
# 4. EVENTOS DE WEBSOCKET (Comunicación en tiempo real)
# ============================================

@socketio.on('connect')
def handle_connect():
    """
    Se ejecuta cuando un usuario se conecta al chat
    Envía un mensaje de bienvenida personalizado
    """
    print(f'Cliente conectado: {request.sid}')

    # Crear mensaje de bienvenida usando la configuración del agente
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

    # Enviar el mensaje de bienvenida al usuario que se conectó
    emit('mensaje_bot', {
        'texto': mensaje_bienvenida,
        'timestamp': datetime.now().strftime('%H:%M:%S')
    })

@socketio.on('disconnect')
def handle_disconnect():
    """
    Se ejecuta cuando un usuario se desconecta
    Limpia su historial para liberar memoria
    """
    print(f'Cliente desconectado: {request.sid}')
    if request.sid in conversacion_historial:
        del conversacion_historial[request.sid]

@socketio.on('enviar_mensaje')
def handle_mensaje(data):
    """
    Se ejecuta cuando el usuario envía un mensaje
    1. Recibe el mensaje
    2. Lo muestra en el chat
    3. Obtiene respuesta de Gemini
    4. Envía la respuesta al usuario
    """
    mensaje = data.get('mensaje', '')
    timestamp = datetime.now().strftime('%H:%M:%S')

    if mensaje:
        print(f"[{timestamp}] Cliente {request.sid[:8]}: {mensaje}")

        # Mostrar el mensaje del usuario en el chat
        emit('nuevo_mensaje', {
            'cliente_id': request.sid[:8],
            'mensaje': mensaje,
            'timestamp': timestamp,
            'es_usuario': True
        }, broadcast=True)

        # Mostrar que el bot está "escribiendo..."
        emit('bot_escribiendo', {'estado': True})

        # Obtener respuesta de Gemini
        respuesta_bot = obtener_respuesta_gemini(mensaje, request.sid)

        # Enviar la respuesta del bot al chat
        emit('mensaje_bot', {
            'texto': respuesta_bot,
            'timestamp': datetime.now().strftime('%H:%M:%S')
        }, broadcast=True)

        # Ocultar el indicador de "escribiendo..."
        emit('bot_escribiendo', {'estado': False})

@socketio.on('limpiar_chat')
def handle_limpiar():
    """
    Se ejecuta cuando el usuario hace clic en "Limpiar chat"
    Borra el historial de conversación
    """
    if request.sid in conversacion_historial:
        conversacion_historial[request.sid] = []
    emit('chat_limpiado', {})

# ============================================
# 5. INICIAR EL SERVIDOR
# ============================================

if __name__ == '__main__':
    # Mostrar información de inicio
    print(f"""
    ========================================
    🤖 CHATBOT CON GEMINI INICIADO
    ========================================
    Agente: {AGENTE_CONFIG['nombre']}
    Especialidad: {AGENTE_CONFIG['rubro']}
    URL: http://localhost:5001
    ========================================
    Presiona Ctrl+C para detener el servidor
    """)

    # Iniciar el servidor en el puerto 5001
    socketio.run(app, debug=True, port=5001)
