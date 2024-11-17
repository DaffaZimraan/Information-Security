import socket
from des import encrypt, decrypt  
from rsa import generate_keys, encrypt as rsa_encrypt, decrypt as rsa_decrypt

def client_program():
    host = socket.gethostname()  
    port = 5000 
    pka_host = socket.gethostname()
    pka_port = 5001 

    client_private_key, client_public_key = generate_keys()
    
    # Print Server keys
    print("Client Keys:")
    print(f"Public Key (e, n): {client_public_key}")
    print(f"Private Key (d, n): {client_private_key}\n")
    
    pka_socket = socket.socket()
    pka_socket.connect((pka_host, pka_port))
    
    #If already connected to pka, send the client's public key to pka and print the log
    pka_socket.send(f"{client_public_key}".encode())  # Send as a string
    print("Client Public Key sent to PKA.")
    
    pka_public_key = pka_socket.recv(1024).decode()
    print(f"Received PKA Public Key: {pka_public_key}")
    pka_socket.close()
    
    # Request server public key from PKA
    pka_socket = socket.socket()
    pka_socket.connect((pka_host, pka_port))
    pka_socket.send("REQUEST:SERVER".encode())  # Request server public key
    server_public_key = pka_socket.recv(1024).decode()
    print(f"Received Server Public Key from PKA: {server_public_key}")
    pka_socket.close()
    
    client_socket = socket.socket()
    client_socket.connect((host, port))

    des_key = client_socket.recv(1024)  
    print(f"Received generated DES key: {des_key.hex()}")

    message = input("Type your message here (exit): ")

    while message.lower().strip() != 'exit':
        print("Waiting for server to response ...")
        encrypted_message = encrypt(message, des_key)
        client_socket.send(encrypted_message)

        encrypted_response = client_socket.recv(1024)
        if encrypted_response == b'exit':
            print("Server has disconnected.")
            break  
        
        print(f"This is the original message from server (encrypted): {encrypted_response.hex()}")
        response = decrypt(encrypted_response, des_key)
        print("\nFrom server:", response)

        message = input("Type your message here (exit): ")

    client_socket.close()

if __name__ == '__main__':
    client_program()
