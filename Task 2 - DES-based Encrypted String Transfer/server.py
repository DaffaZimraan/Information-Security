import socket
from des import generate_key, encrypt, decrypt  

def server_program():
    host = socket.gethostname()
    port = 5000  

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(1)
    
    print("Server is waiting for connections...")
    conn, address = server_socket.accept()
    print("Connection from:", address)

    des_key = generate_key() 
    print(f"\nThis is the generated key: {des_key.hex()}")
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
