import socket
import threading

def manejar_cliente(conn, addr):
    """Maneja la conexión con un cliente específico"""
    print(f"[NUEVA CONEXIÓN] {addr} conectado.")

    conectado = True
    while conectado:
        try:
            # Recibir mensaje del cliente
            mensaje = conn.recv(1024).decode('utf-8')

            if not mensaje:
                break

            if mensaje.lower() == 'salir':
                print(f"[{addr}] se desconectó.")
                conectado = False
            else:
                print(f"[{addr}] {mensaje}")

                # Respuesta simple del servidor
                respuesta = f"Servidor recibió: {mensaje}"
                conn.send(respuesta.encode('utf-8'))

        except ConnectionResetError:
            print(f"[ERROR] Conexión perdida con {addr}")
            break

    conn.close()

def iniciar_servidor():
    """Inicia el servidor de chat"""
    # Configuración del servidor
    HOST = '127.0.0.1'  # localhost
    PUERTO = 5555

    # Crear socket del servidor
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PUERTO))
    servidor.listen(5)

    print(f"[SERVIDOR INICIADO] Escuchando en {HOST}:{PUERTO}")
    print("[ESPERANDO CONEXIONES...]")

    while True:
        try:
            # Aceptar nuevas conexiones
            conn, addr = servidor.accept()

            # Crear un thread para manejar cada cliente
            thread = threading.Thread(target=manejar_cliente, args=(conn, addr))
            thread.start()

            print(f"[CONEXIONES ACTIVAS] {threading.active_count() - 1}")

        except KeyboardInterrupt:
            print("\n[SERVIDOR] Apagando servidor...")
            break

    servidor.close()

if __name__ == "__main__":
    iniciar_servidor()