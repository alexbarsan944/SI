import socket
from cbc import CBC
from ecb import ECB


def server_program():
    host = socket.gethostname()
    port = 5000
    key_to_encrypt_keys = b'veryawesomekeyyy'
    key_for_CBC = 'best key for cbc'
    key_for_ECB = 'best key for ecb'

    server_socket = socket.socket()  # get instance
    server_socket.bind((host, port))  # bind host address and port together

    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break

        if str(data) == 'ECB':
            temp = ECB(key_for_ECB, key_to_encrypt_keys)
            to_send = temp.encrypt(key_for_ECB)

            conn.send(to_send.encode())  # send data to the client
            mesaj = conn.recv(1024).decode()

            if str(mesaj) == 'ready to communicate':
                text_de_trimis = 'ana are ECB'
                temp2 = ECB(text_de_trimis, key_for_ECB.encode())
                crypto = temp2.encrypt(text_de_trimis)
                conn.send(crypto.encode())

        if str(data) == 'CBC':
            temp = CBC(key_for_CBC, key_to_encrypt_keys)
            to_send_key = temp.encrypt(key_for_CBC)
            to_send_iv = temp.iv

            conn.send(to_send_key.encode())  # send data to the client
            conn.send(str(to_send_iv).encode())

            mesaj = conn.recv(1024).decode()

            #  poate incepe comunicarea
            if str(mesaj) == 'ready to communicate':
                text_de_trimis = 'ana are CBC'
                temp2 = CBC(text_de_trimis, key_for_CBC.encode())
                iv = temp2.iv
                crypto = temp2.encrypt(text_de_trimis)
                conn.send(crypto.encode())
                conn.send(str(iv).encode())

    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()
