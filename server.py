import socket
import threading
import ssl

# Global variable to store voted clients
voted_clients = set()

def handle_client(client_socket):
    try:
        # Receive client's name and CNIC
        client_socket.sendall(b"Enter your name: ")
        name = client_socket.recv(1024).decode().strip()
        client_socket.sendall(b"Enter your CNIC: ")
        cnic = client_socket.recv(1024).decode().strip()

        # Check if voter is in the list and has not voted before
        if name + " " + cnic in voted_clients:
            client_socket.sendall(b"You have already voted.\n")
        else:
            with open("Voters_List.txt", "r") as f:
                voters_list = f.readlines()
                for voter in voters_list:
                    if name in voter and cnic in voter:
                        client_socket.sendall(b"Welcome!\n")
                        # Display candidates and poll symbols
                        with open("Candidates_List.txt", "r") as candidates_file:
                            candidates = candidates_file.read()
                            client_socket.sendall(candidates.encode())
                        
                        # Receive and record vote
                        client_socket.sendall(b"Enter the poll symbol of your chosen candidate: ")
                        vote = client_socket.recv(1024).decode().strip()
                        with open("Votes_Record.txt", "a") as votes_file:
                            votes_file.write(name + " " + cnic + " " + vote + "\n")
                        # Add client to voted clients set
                        voted_clients.add(name + " " + cnic)
                        break
                else:
                    client_socket.sendall(b"You are not authorized to vote or your credentials are incorrect.\n")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('domain.crt', 'domain.key')
    server_socket = context.wrap_socket(server, server_side=True)
    server_socket.bind(('192.168.41.216', 9998))
    server_socket.listen(5)
    print("Server is listening...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr} has been established!")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main()
