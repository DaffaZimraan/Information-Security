import socket
from des import encrypt, decrypt  

def client_program():
    host = socket.gethostname()  
    port = 5000  

    client_socket = socket.socket()
    client_socket.connect((host, port))

    des_key = client_socket.recv(1024)  
    print(f"Received generated key: {des_key.hex()}")

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
