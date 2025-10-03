# 🤖 Proyecto Chatbots en Python

Este proyecto contiene **dos chatbots** diferentes, cada uno en su propia carpeta. Ambos usan la misma interfaz web pero funcionan de manera distinta.

---

## 📁 Estructura del Proyecto

```
ChatbotPython/
├── chatbot-gemini/          # Chatbot con Inteligencia Artificial (Google Gemini)
│   ├── servidor.py
│   ├── config.py
│   ├── requirements.txt
│   └── templates/
│       └── chat.html
│
├── chatbot-sockets/         # Chatbot Simple (solo retransmite mensajes)
│   ├── servidor.py
│   ├── requirements.txt
│   └── templates/
│       └── chat.html
│
└── README.md               # Este archivo
```

---

## 🚀 Instrucciones de Ejecución

### ⚙️ Requisitos Previos

1. **Python 3.8 o superior** instalado en tu computadora
2. **pip** (viene incluido con Python)

Para verificar que tienes Python instalado, abre una terminal y ejecuta:
```bash
python --version
```

---

## 1️⃣ Chatbot con Gemini (Inteligencia Artificial)

Este chatbot usa la API de Google Gemini para responder de manera inteligente.

### 📝 Pasos para ejecutarlo:

#### Paso 1: Ir a la carpeta
```bash
cd chatbot-gemini
```

#### Paso 2: Instalar las dependencias
```bash
pip install -r requirements.txt
```

#### Paso 3: Configurar la API Key de Gemini

1. Abre el archivo `config.py`
2. Reemplaza la API key con la tuya propia:
   ```python
   GEMINI_API_KEY = "TU_API_KEY_AQUI"
   ```
3. Si no tienes una API key, obtén una gratis en: https://makersuite.google.com/app/apikey

#### Paso 4: Ejecutar el servidor
```bash
python servidor.py
```

#### Paso 5: Abrir el navegador
Ve a: **http://localhost:5001**

### ✅ ¡Listo! Ahora puedes chatear con el bot inteligente.

---

## 2️⃣ Chatbot Simple (WebSockets)

Este chatbot solo retransmite mensajes entre usuarios. No usa inteligencia artificial.

### 📝 Pasos para ejecutarlo:

#### Paso 1: Ir a la carpeta
```bash
cd chatbot-sockets
```

#### Paso 2: Instalar las dependencias
```bash
pip install -r requirements.txt
```

#### Paso 3: Ejecutar el servidor
```bash
python servidor.py
```

#### Paso 4: Abrir el navegador
Ve a: **http://localhost:5000**

### ✅ ¡Listo! Ahora tienes un chat simple funcionando.

---

## 🔄 Ejecutar Ambos al Mismo Tiempo

**Sí, puedes ejecutar ambos chatbots a la vez** porque usan puertos diferentes:

- **Chatbot Gemini:** Puerto 5001 → http://localhost:5001
- **Chatbot Simple:** Puerto 5000 → http://localhost:5000

### Pasos:

1. Abre **dos terminales** (o dos ventanas de PowerShell/CMD)
2. En la primera terminal:
   ```bash
   cd chatbot-gemini
   python servidor.py
   ```
3. En la segunda terminal:
   ```bash
   cd chatbot-sockets
   python servidor.py
   ```
4. Abre dos pestañas en tu navegador:
   - Pestaña 1: http://localhost:5001 (Gemini)
   - Pestaña 2: http://localhost:5000 (Simple)

---

## 🛠️ Personalizar el Chatbot de Gemini

Puedes cambiar la personalidad y especialidad del bot editando `chatbot-gemini/config.py`:

```python
AGENTE_CONFIG = {
    "nombre": "NombreDelBot",
    "rubro": "especialidad del bot",
    "personalidad": "cómo se comporta",
    "instrucciones_especiales": """
    Instrucciones detalladas aquí...
    """
}
```

**Ejemplos de rubros:**
- Asistente médico
- Tutor de programación
- Chef virtual
- Asesor financiero
- Entrenador personal

---

## 🐛 Solución de Problemas

### Error: "No module named flask"
**Solución:** Instala las dependencias:
```bash
pip install -r requirements.txt
```

### Error: "Address already in use" (Puerto ocupado)
**Solución:**
- Cierra cualquier servidor anterior que esté corriendo
- O cambia el puerto en `servidor.py`:
  ```python
  socketio.run(app, debug=True, port=NUEVO_PUERTO)
  ```

### El bot de Gemini no responde
**Solución:**
- Verifica que tu API key sea correcta en `config.py`
- Asegúrate de tener conexión a Internet
- Revisa que no hayas excedido el límite gratuito de la API

---

## 📚 Tecnologías Usadas

- **Python 3.x** - Lenguaje de programación
- **Flask** - Framework web
- **Flask-SocketIO** - WebSockets para comunicación en tiempo real
- **Google Gemini API** - Inteligencia artificial (solo chatbot-gemini)

---

## 📄 Licencia

Este proyecto es de código abierto y está disponible para uso educativo.

---

## 🆘 Ayuda

Si tienes problemas, verifica:
1. ✅ Python instalado correctamente
2. ✅ Dependencias instaladas (`pip install -r requirements.txt`)
3. ✅ API key configurada (solo para chatbot-gemini)
4. ✅ Puerto no ocupado por otra aplicación

---

**¡Disfruta tus chatbots! 🎉**
