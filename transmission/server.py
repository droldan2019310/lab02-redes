import socket

def start_server(host="127.0.0.1", port=5050):  # ← puerto fijo
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"[SERVER] Escuchando en {host}:{port}...")

    conn, addr = server_socket.accept()
    print(f"[SERVER] Conexión recibida de {addr}")

    data = conn.recv(65536).decode()
    print(f"[SERVER] Trama recibida: {data[:64]}... (longitud {len(data)})")

    conn.close()
    return data

if __name__ == "__main__":
    msg = start_server()
    print(f"[SERVER] Mensaje recibido: {msg}")
