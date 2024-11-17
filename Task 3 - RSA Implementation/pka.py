import socket
from rsa import generate_keys, encrypt, decrypt

def pka_program():
    # Generate PKA RSA key pair
    pka_private_key, pka_public_key = generate_keys()
    
    # Print PKA keys
    print("PKA Keys:")
    print(f"Public Key (e, n): {pka_public_key}")
    print(f"Private Key (d, n): {pka_private_key}\n")

    host = socket.gethostname()
    port = 5001  # PKA listens here
    pka_socket = socket.socket()
    pka_socket.bind((host, port))
    pka_socket.listen(2)
    
    server_public_key = None
    client_public_key = None
    
    # After someone connect, receive their public key and print it
    # When server connects get its public key
    conn, address = pka_socket.accept()
    print(f"Connection from {address} established.")
    server_public_key = conn.recv(1024).decode()  # Assume public key is sent as a string
    print(f"Received Server Public Key: {server_public_key}")
    
    # Send PKA public key to server
    conn.send(f"{pka_public_key}".encode())  # Send PKA public key as a string
    print("Sent PKA Public Key to Server.")
    conn.close()
    
    # When client connects get its public key
    conn, address = pka_socket.accept()
    print(f"Connection from {address} established.")
    client_public_key = conn.recv(1024).decode()  # Assume public key is sent as a string
    print(f"Received Client Public Key: {client_public_key}")
    
    # Send PKA public key to client
    conn.send(f"{pka_public_key}".encode())  # Send PKA public key as a string
    print("Sent PKA Public Key to Client.")
    conn.close()
    
    # Print both keys
    print("\nPublic keys received:")
    print(f"Server Public Key: {server_public_key}")
    print(f"Client Public Key: {client_public_key}")
    
    print("PKA is ready for key exchange...")

    # Ready to handle request such as request server public key or client public key
    # Make sure both server and client connected first before continue
    while True:
        conn, address = pka_socket.accept()
        print(f"Connection from {address} established for key request.")
        request = conn.recv(1024).decode()  # Request format: "REQUEST:<type>"
        
        if request == "REQUEST:SERVER":
            print("Sending Server Public Key to Client...")
            conn.send(f"{server_public_key}".encode())
        elif request == "REQUEST:CLIENT":
            print("Sending Client Public Key to Server...")
            conn.send(f"{client_public_key}".encode())
        else:
            print("Invalid request received.")
            conn.send("ERROR: Invalid request.".encode())
        conn.close()

if __name__ == "__main__":
    pka_program()
