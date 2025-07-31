import socket

def send_message(message, host="127.0.0.1", port=5050):  # ← puerto fijo
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        client_socket.sendall(message.encode())
        print(f"[CLIENT] Trama enviada ({len(message)} bits): {message[:64]}...")
        client_socket.close()
    except Exception as e:
        print(f"[CLIENT] Error al enviar mensaje: {e}")

if __name__ == "__main__":
    test_message = input("Mensaje a enviar (prueba): ").strip()
    send_message(test_message)
