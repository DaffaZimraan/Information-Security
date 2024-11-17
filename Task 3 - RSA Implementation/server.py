import socket
from des import generate_key, encrypt, decrypt  
from rsa import generate_keys, encrypt as rsa_encrypt, decrypt as rsa_decrypt
import time

def server_program():
    host = socket.gethostname()
    port = 5000
    pka_host = socket.gethostname()
    pka_port = 5001
    
    server_private_key, server_public_key = generate_keys()   
    
    # Print Server keys
    print("Server Keys:")
    print(f"Public Key (e, n): {server_public_key}")
    print(f"Private Key (d, n): {server_private_key}\n")
    
    pka_socket = socket.socket()
    pka_socket.connect((pka_host, pka_port))
    
    #If already connected to pka, send the server's public key to pka and print the log
    pka_socket.send(f"{server_public_key}".encode())  # Send as a string
    print("Server Public Key sent to PKA.")
    
    # Receive PKA public key
    pka_public_key = pka_socket.recv(1024).decode()
    print(f"Received PKA Public Key: {pka_public_key}")
    pka_socket.close()
    
    # Wait for the client to register its key with PKA
    print("Waiting for client to register its public key with PKA...")
    time.sleep(5)  # Adjust the duration based on expected client startup time
    
    #Request client public key to pka
    pka_socket = socket.socket()
    pka_socket.connect((pka_host, pka_port))
    pka_socket.send("REQUEST:CLIENT".encode())  # Request client public key
    client_public_key = pka_socket.recv(1024).decode()
    print(f"Received Client Public Key from PKA: {client_public_key}")
    pka_socket.close()
    
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(1)
    
    print("Server is waiting for connections...")
    conn, address = server_socket.accept()
    print("Connection from:", address)

    des_key = generate_key() 
    print(f"\nGenerated DES key: {des_key.hex()}")
    conn.send(des_key)  

    while True:
        encrypted_data = conn.recv(1024)
        
        if not encrypted_data:
            print("Client Disconnected.")
            break
            
        print(f"This is the original message from client (encrypted): {encrypted_data.hex()}")
        
        message = decrypt(encrypted_data, des_key)
        print("\nFrom connected client:", message)

        reply_message = input("Type your message here (exit): ")
        if reply_message.lower() == 'exit':
            conn.send(b'exit')
            print("Server is shutting down...")
            break
        
        print("Waiting for client to response...")
        encrypted_reply = encrypt(reply_message, des_key)
        conn.send(encrypted_reply)

    conn.close()

if __name__ == '__main__':
    server_program()
