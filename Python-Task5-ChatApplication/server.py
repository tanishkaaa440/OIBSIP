import socket
import threading
from datetime import datetime

HOST = "127.0.0.1"  # localhost = this computer only
PORT = 5555

clients = {}  # connection -> username
lock = threading.Lock()


def timestamp():
    return datetime.now().strftime("%H:%M")


def broadcast(message, sender=None):
    """Send message to everyone except the sender."""
    with lock:
        for conn in list(clients):
            if conn is not sender:
                try:
                    conn.sendall((message + "\n").encode("utf-8"))
                except OSError:
                    pass


def handle_client(conn, addr):
    name = None
    try:
        name = conn.recv(1024).decode("utf-8").strip() or "Unknown"
        with lock:
            clients[conn] = name
        print(f"[{timestamp()}] {name} connected from {addr}")
        broadcast(f"[{timestamp()}] *** {name} joined the chat ***", conn)

        while True:
            data = conn.recv(1024)
            if not data:  # empty = client closed connection
                break
            text = data.decode("utf-8").strip()
            if text:
                broadcast(f"[{timestamp()}] {name}: {text}", conn)
    except (ConnectionResetError, OSError):
        pass
    finally:
        with lock:
            clients.pop(conn, None)
        conn.close()
        if name:
            print(f"[{timestamp()}] {name} disconnected")
            broadcast(f"[{timestamp()}] *** {name} left the chat ***")


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server listening on {HOST}:{PORT} (Ctrl+C to stop)")

    try:
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.close()


if __name__ == "__main__":
    main()
    