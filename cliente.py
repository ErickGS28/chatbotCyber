import socket

def iniciar_cliente():
    """Inicia el cliente de chat"""
    # Configuración del cliente
    HOST = '127.0.0.1'  # localhost
    PUERTO = 5555

    # Crear socket del cliente
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Conectar al servidor
        cliente.connect((HOST, PUERTO))
        print(f"[CONECTADO] Conectado al servidor {HOST}:{PUERTO}")
        print("Escribe tus mensajes (escribe 'salir' para desconectar):\n")

        while True:
            # Enviar mensaje
            mensaje = input("Tú: ")

            if not mensaje:
                continue

            cliente.send(mensaje.encode('utf-8'))

            if mensaje.lower() == 'salir':
                print("[DESCONECTANDO] Cerrando conexión...")
                break

            # Recibir respuesta del servidor
            try:
                respuesta = cliente.recv(1024).decode('utf-8')
                print(f"Servidor: {respuesta}")
            except:
                print("[ERROR] No se pudo recibir respuesta del servidor")
                break

    except ConnectionRefusedError:
        print("[ERROR] No se pudo conectar al servidor. Asegúrate de que el servidor esté ejecutándose.")
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        cliente.close()
        print("[DESCONECTADO] Conexión cerrada.")

if __name__ == "__main__":
    iniciar_cliente()