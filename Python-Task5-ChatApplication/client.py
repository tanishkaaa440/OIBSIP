import os
import socket
import threading
from datetime import datetime

HOST = "127.0.0.1"
PORT = 5555


def timestamp():
    return datetime.now().strftime("%H:%M")


def receive_messages(sock):
    """Runs in background: print anything the server sends."""
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            print(data.decode("utf-8"), end="")
        except OSError:
            break
    print("\nDisconnected from server.")
    os._exit(0)  # close whole program


def main():
    name = input("Enter your name: ").strip()
    if not name:
        name = "Anonymous"

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))
    except ConnectionRefusedError:
        print("Cannot connect. Is server.py running?")
        return

    sock.sendall(name.encode("utf-8"))
    threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

    print("Connected! Type a message and press Enter. Type 'quit' to leave.\n")
    while True:
        try:
            message = input()
        except (EOFError, KeyboardInterrupt):
            break
        if message.lower() == "quit":
            break
        if message.strip():
            try:
                sock.sendall(message.encode("utf-8"))
                print(f"[{timestamp()}] {name}: {message}")
            except OSError:
                break
    sock.close()


if __name__ == "__main__":
    main()