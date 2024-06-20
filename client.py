import socket
import ssl

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations('domain.crt')
    context.check_hostname = False
    client_socket = context.wrap_socket(client)
    client_socket.connect(('192.168.41.216', 9998))

    try:
        print(client_socket.recv(1024).decode(), end="")
        name = input()
        client_socket.sendall(name.encode())

        print(client_socket.recv(1024).decode(), end="")
        cnic = input()
        client_socket.sendall(cnic.encode())

        response = client_socket.recv(1024).decode()
        print(response)

        if "Welcome" in response:
            candidates = client_socket.recv(1024).decode()
            print(candidates)

            print(client_socket.recv(1024).decode(), end="")
            vote = input()
            client_socket.sendall(vote.encode())
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
