# 🤖 Proyecto Chatbot Python - Sistema de Chat Seguro

**Versión Actual:** 3.0 con SHA256 y MD5
**Fecha:** 20 de Octubre 2025

Sistema de chat multiusuario con múltiples versiones que implementan diferentes niveles de seguridad de manera incremental.

---

## 📁 Estructura del Proyecto

```
ChatbotPython/
├── 📂 versiones/                      [Todas las versiones históricas]
│   ├── v1.0_chat-basico/              (Chat simple sin cifrado)
│   ├── v2.0_cifrado-separado/         (Con cifrado AES/RSA)
│   └── v3.0_con-sha256-md5/           (Con SHA256 + MD5) ⭐ ACTUAL
│
├── 📂 chatbot-simetrico/              [Versión de trabajo - AES]
├── 📂 chatbot-asimetrico/             [Versión de trabajo - RSA]
├── 📂 extra/chatbot-gemini/           [Chatbot con IA de Google]
│
├── 📄 cambios.txt                     ⭐ Registro de cambios con MD5
├── 📄 README.md                       📖 Este archivo
├── 📄 README_ESTRUCTURA.txt           📖 Guía de estructura de versiones
└── 📄 PROYECTO_EXPLICACION.txt        📖 Documentación técnica detallada
```

---

## 🚀 Inicio Rápido

### Opción 1: Ejecutar la Versión Más Completa (Recomendado)

**Chatbot con Cifrado Simétrico + SHA256 (Puerto 5001):**

```bash
cd versiones/v3.0_con-sha256-md5/chatbot-simetrico
pip install -r requirements.txt
python servidor.py
```

Abre en tu navegador: **http://localhost:5001**

**Chatbot con Cifrado Asimétrico + SHA256 (Puerto 5002):**

```bash
cd versiones/v3.0_con-sha256-md5/chatbot-asimetrico
pip install -r requirements.txt
python servidor.py
```

Abre en tu navegador: **http://localhost:5002**

### Opción 2: Trabajar con Versiones de Desarrollo

```bash
cd chatbot-simetrico    # Puerto 5001
cd chatbot-asimetrico   # Puerto 5002
```

---

## 📋 Historial de Versiones

### 📦 Versión 1.0 - Chat Básico (01/10/2025)

**Ubicación:** `versiones/v1.0_chat-basico/`

**Características:**
- ✅ Chat multiusuario en tiempo real
- ✅ WebSockets
- ✅ Lista de usuarios conectados
- ❌ Sin cifrado
- ❌ Sin SHA256

**Puerto:** 5000
**MD5:** `d0b4616be17c6d2428ade276eedef35c`

---

### 📦 Versión 2.0 - Con Cifrado (10/10/2025)

**Ubicación:** `versiones/v2.0_cifrado-separado/`

**Versión Simétrica (AES):**
- ✅ Chat multiusuario
- ✅ Cifrado simétrico con AES (Fernet)
- ✅ Una sola llave compartida
- ❌ Sin SHA256

**Puerto:** 5001
**MD5:** `4d6065ac226697f678dc11f614dddede`

**Versión Asimétrica (RSA):**
- ✅ Chat multiusuario
- ✅ Cifrado asimétrico con RSA-2048
- ✅ Llaves pública/privada
- ❌ Sin SHA256

**Puerto:** 5002
**MD5:** `d9d3280d63f28cac0f50a472c90f29f9`

---

### 📦 Versión 3.0 - Con SHA256 y MD5 (20/10/2025) ⭐ ACTUAL

**Ubicación:** `versiones/v3.0_con-sha256-md5/`

**Versión Simétrica (AES + SHA256):**
- ✅ Chat multiusuario
- ✅ Cifrado simétrico con AES
- ✅ Hash SHA256 para verificar integridad de mensajes
- ✅ Función `hashear_mensaje()` - genera SHA256
- ✅ Función `verificar_hash()` - valida integridad
- ✅ MD5 para verificar integridad de archivos

**Puerto:** 5001
**MD5:** `f33661df2d9ad515be5f4cda0ff556a5`

**Versión Asimétrica (RSA + SHA256):**
- ✅ Chat multiusuario
- ✅ Cifrado asimétrico con RSA-2048
- ✅ Hash SHA256 para verificar integridad de mensajes
- ✅ Función `hashear_mensaje()` - genera SHA256
- ✅ Función `verificar_hash()` - valida integridad
- ✅ MD5 para verificar integridad de archivos

**Puerto:** 5002
**MD5:** `fe2815eb7c32d05434eeda0656b3c676`

---

## 🔐 Diferencias entre Cifrado Simétrico y Asimétrico

| Característica | Simétrico (AES) | Asimétrico (RSA) |
|----------------|-----------------|-------------------|
| **Velocidad** | ⚡ Más rápido | ⏱️ Más lento |
| **Recursos** | 💻 Menos recursos | 🖥️ Más recursos |
| **Seguridad** | 🔒 Seguro | 🔐 Más seguro |
| **Llaves** | 🔑 Una sola llave | 🔑🔑 Pública + Privada |
| **Uso ideal** | Chat rápido interno | Intercambio seguro |
| **Puerto** | 5001 | 5002 |
| **Interfaz** | 💜 Morado | 💗 Rosa |

### Características Comunes (v3.0)

- ✅ Chat multiusuario en tiempo real
- ✅ Verificación de integridad con SHA256
- ✅ Interfaz web moderna y responsiva
- ✅ WebSockets para comunicación instantánea
- ✅ Lista de usuarios conectados en tiempo real
- ✅ Notificaciones de entrada/salida
- ✅ MD5 para verificar archivos del proyecto

---

## 🛠️ Cómo Ejecutar Diferentes Versiones

Cada versión tiene su archivo `instrucciones.txt` con pasos detallados:

### Versión 1.0 (Chat Básico)
```bash
cd versiones/v1.0_chat-basico
pip install -r requirements.txt
python servidor.py
# → http://localhost:5000
```

### Versión 2.0 Simétrica (AES)
```bash
cd versiones/v2.0_cifrado-separado/chatbot-simetrico
pip install -r requirements.txt
python servidor.py
# → http://localhost:5001
```

### Versión 2.0 Asimétrica (RSA)
```bash
cd versiones/v2.0_cifrado-separado/chatbot-asimetrico
pip install -r requirements.txt
python servidor.py
# → http://localhost:5002
```

### Versión 3.0 Simétrica (AES + SHA256) ⭐
```bash
cd versiones/v3.0_con-sha256-md5/chatbot-simetrico
pip install -r requirements.txt
python servidor.py
# → http://localhost:5001
```

### Versión 3.0 Asimétrica (RSA + SHA256) ⭐
```bash
cd versiones/v3.0_con-sha256-md5/chatbot-asimetrico
pip install -r requirements.txt
python servidor.py
# → http://localhost:5002
```

---

## 🔄 Ejecutar Múltiples Versiones Simultáneamente

Puedes ejecutar diferentes versiones al mismo tiempo porque usan puertos diferentes:

1. **Abre múltiples terminales**
2. **En cada terminal, ejecuta una versión diferente**
3. **Abre pestañas del navegador para cada puerto**

Ejemplo:
- Terminal 1: v3.0 simétrica → `http://localhost:5001`
- Terminal 2: v3.0 asimétrica → `http://localhost:5002`

---

## 📄 Archivos Importantes

### 📄 cambios.txt
Registro oficial de cambios con hashes MD5 de cada versión.

**Formato:**
```
Fecha de implementación - Lo que se hizo
SW - nombre del archivo = hash en md5
```

Usa este archivo para verificar la integridad de los archivos del proyecto.

### 📄 README_ESTRUCTURA.txt
Guía completa de la estructura del proyecto y cómo navegar entre versiones.

### 📄 PROYECTO_EXPLICACION.txt
Explicación técnica detallada del proyecto:
- Conceptos de cifrado (AES, RSA)
- Explicación de SHA256 y MD5
- Ejemplos prácticos
- Glosario de términos

### 📄 instrucciones.txt (en cada versión)
Pasos específicos para ejecutar esa versión particular.

---

## 🔍 Verificar Integridad de Archivos

Cada archivo Python tiene un hash MD5 documentado en `cambios.txt`.

### Calcular MD5 de un archivo:

**Python:**
```bash
python -c "import hashlib; print(hashlib.md5(open('archivo.py','rb').read()).hexdigest())"
```

**PowerShell (Windows):**
```powershell
Get-FileHash -Algorithm MD5 archivo.py
```

**Linux/Mac:**
```bash
md5sum archivo.py
```

### Comparar con MD5 registrado:
- ✅ **Coinciden:** Archivo íntegro, sin modificaciones
- ⚠️ **No coinciden:** Archivo modificado

---

## 🐛 Solución de Problemas

### ❌ Error: "No module named flask"
**Solución:**
```bash
pip install -r requirements.txt
```

### ❌ Error: "Address already in use" (Puerto ocupado)
**Solución:**
1. Cierra servidores anteriores (Ctrl+C)
2. O cambia el puerto en `servidor.py`:
   ```python
   socketio.run(app, debug=True, port=NUEVO_PUERTO)
   ```

### ❌ No veo mensajes en el chat
**Solución:**
1. Verifica que el servidor esté corriendo
2. Refresca el navegador (F5)
3. Abre la consola del navegador (F12) para ver errores

### ❌ Error al instalar dependencias
**Solución:**
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## 📚 Tecnologías Usadas

- **Python 3.8+** - Lenguaje de programación
- **Flask** - Framework web
- **Flask-SocketIO** - WebSockets para comunicación en tiempo real
- **Cryptography** - Librería de cifrado (AES, RSA)
- **Hashlib** - Librería de hashing (SHA256, MD5)

---

## 🎯 Casos de Uso

### Versión 1.0 (Chat Básico)
- Aprender WebSockets
- Prototipo rápido
- Comunicación sin requisitos de seguridad

### Versión 2.0 (Con Cifrado)
- Chat interno de equipo
- Comunicación en LAN
- Aprender conceptos de cifrado

### Versión 3.0 (SHA256 + MD5) ⭐
- Comunicación segura con verificación de integridad
- Proyecto educativo completo de seguridad
- Base para aplicaciones de producción

---

## 🌟 Chatbot Extra: Gemini con IA

Este proyecto también incluye un chatbot con inteligencia artificial usando Google Gemini.

**Ubicación:** `extra/chatbot-gemini/`

**Instrucciones:** Ver `extra/chatbot-gemini/instrucciones_ejecucion.txt`

---

## ⚠️ Importante

- ❗ **NO elimines** la carpeta `versiones/` - contiene el historial del proyecto
- ❗ **NO modifiques** los archivos en `versiones/` - son versiones de respaldo
- ❗ Trabaja en las carpetas `chatbot-simetrico/` o `chatbot-asimetrico/` de la raíz
- ❗ Actualiza `cambios.txt` si modificas algún archivo de código

---

## 📞 Soporte

Para problemas o dudas, consulta:

1. ✅ `README_ESTRUCTURA.txt` - Estructura del proyecto
2. ✅ `PROYECTO_EXPLICACION.txt` - Documentación técnica
3. ✅ `cambios.txt` - Registro de cambios y MD5
4. ✅ `instrucciones.txt` (en cada versión) - Cómo ejecutar cada versión

---

## 📊 Registro de Cambios

| Fecha | Versión | Descripción |
|-------|---------|-------------|
| 01/10/2025 | 1.0 | Chat básico sin cifrado |
| 10/10/2025 | 2.0 | Implementación de cifrado (AES y RSA) |
| 20/10/2025 | 3.0 | Implementación de SHA256 y MD5 ⭐ |

Ver detalles completos en `cambios.txt`.

---

## 🎓 Glosario Básico

- **Cifrado:** Convertir texto legible en código secreto
- **Descifrado:** Convertir código secreto en texto legible
- **Hash:** Huella digital única de datos
- **SHA256:** Algoritmo de hashing seguro (256 bits)
- **MD5:** Algoritmo de hashing para verificar integridad de archivos
- **AES:** Cifrado simétrico rápido y seguro
- **RSA:** Cifrado asimétrico con llaves pública/privada
- **WebSocket:** Protocolo de comunicación bidireccional en tiempo real
- **Flask:** Framework web minimalista para Python

---

## 📅 Última Actualización

**Fecha:** 20 de Octubre 2025
**Versión:** 3.0 con SHA256 y MD5
**Ubicación:** C:\Users\eeeri\Downloads\ChatbotPython

---

**¡Disfruta tu chatbot seguro! 🎉**

Para comenzar, elige una versión, sigue las instrucciones y empieza a chatear de forma segura.
