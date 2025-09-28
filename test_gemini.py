import google.generativeai as genai
from config import GEMINI_API_KEY

# Probar la conexión con Gemini
try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash-exp')

    response = model.generate_content("Di 'Hola, la API funciona correctamente!'")
    print("✅ Conexión exitosa con Gemini!")
    print(f"Respuesta: {response.text}")

except Exception as e:
    print(f"❌ Error al conectar con Gemini: {e}")
    print("\nPosibles soluciones:")
    print("1. Verifica que tu API key sea correcta en config.py")
    print("2. Asegúrate de tener conexión a internet")
    print("3. Verifica que la API key esté activa en Google AI Studio")