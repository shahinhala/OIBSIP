import socket
import threading

HOST = "0.0.0.0"
PORT = 5000

clients = {}  # socket -> username
clients_lock = threading.Lock()


def broadcast(message, sender=None):
    """Send a message to all connected clients except an optional sender."""
    with clients_lock:
        recipients = list(clients.keys())

    for client in recipients:
        if client is sender:
            continue
        try:
            client.sendall((message + "\n").encode("utf-8"))
        except OSError:
            remove_client(client)


def remove_client(client):
    with clients_lock:
        username = clients.pop(client, None)

    try:
        client.close()
    except OSError:
        pass

    if username:
        print(f"{username} disconnected.")
        broadcast(f"[Server] {username} left the chat.")


def handle_client(client, address):
    username = "Guest"
    try:
        # First line from a client is the chosen display name.
        file = client.makefile("r", encoding="utf-8", newline="\n")
        requested_name = file.readline().strip()
        if requested_name:
            username = requested_name[:24]

        with clients_lock:
            clients[client] = username

        print(f"{username} connected from {address}.")
        broadcast(f"[Server] {username} joined the chat.", sender=client)
        client.sendall(b"[Server] Connected. Be respectful and do not share private information.\n")

        for line in file:
            message = line.strip()
            if not message:
                continue
            if message.lower() == "/quit":
                break

            print(f"{username}: {message}")
            broadcast(f"{username}: {message}", sender=client)
            # Echo the sender's own message back so their UI can display it.
            try:
                client.sendall(f"You: {message}\n".encode("utf-8"))
            except OSError:
                break

    except (ConnectionError, OSError, UnicodeError) as exc:
        print(f"Connection issue with {address}: {exc}")
    finally:
        try:
            file.close()
        except (UnboundLocalError, OSError):
            pass
        remove_client(client)


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind((HOST, PORT))
        server.listen()
        print(f"Chat server is running on port {PORT}.")
        print("Keep this window open while people are chatting.")
        print("Press Ctrl+C to stop the server.\n")

        while True:
            client, address = server.accept()
            thread = threading.Thread(
                target=handle_client, args=(client, address), daemon=True
            )
            thread.start()

    except KeyboardInterrupt:
        print("\nStopping chat server...")
    except OSError as exc:
        print(f"Could not start server: {exc}")
        print("Check whether port 5000 is already in use.")
    finally:
        with clients_lock:
            connected = list(clients.keys())
        for client in connected:
            try:
                client.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            remove_client(client)
        server.close()


if __name__ == "__main__":
    main()
