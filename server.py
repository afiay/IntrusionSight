#server.py 
import socket
import threading

# Hardcoded list of whitelisted IPs
WHITELISTED_IPS = [
    '127.0.0.1',  # Allow localhost
    '192.168.1.100',  # Example: Replace with actual IPs you want to whitelist
    '10.0.0.1'  # Example: Replace with actual IPs you want to whitelist
]

# Server setup
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 9999))
server.listen()


def handle_client_connection(client_socket, client_ip):
    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break  # Client closed the connection

            print(f"Received message from {client_ip}: {message}")

            # Split the message into command and parameters
            parts = message.split('|')
            if parts[0] == "LOGIN":
                username = parts[1]
                password = parts[2]
                # Here, insert your authentication logic
                # For demonstration, we assume the login is always successful
                if username == "admin" and password == "admin":  # Simplified check
                    response = "Login successful"
                    client_socket.send(response.encode('utf-8'))
                else:
                    response = "Login failed. Check your credentials."
                    client_socket.send(response.encode('utf-8'))
            else:
                response = "Unknown command"
                client_socket.send(response.encode('utf-8'))
    except Exception as e:
        print(f"Error handling connection from {client_ip}: {e}")
    finally:
        print(f"Closing connection from {client_ip}")
        client_socket.close()


def accept_connections(server_socket):
    while True:
        client_socket, client_address = server_socket.accept()
        client_ip = client_address[0]
        if client_ip not in WHITELISTED_IPS:
            print(f"Connection attempt from non-whitelisted IP: {client_ip}")
            client_socket.close()  # Reject the connection
        else:
            print(f"Accepted connection from {client_ip}")
            # Use threading to handle each client connection in parallel
            thread = threading.Thread(
                target=handle_client_connection, args=(client_socket, client_ip))
            thread.start()


if __name__ == "__main__":
    print("Server started, listening for connections...")
    accept_connections(server)
