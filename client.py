import socket
from ecb import ECB
from cbc import CBC
import json


def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number
    key_to_decrypt_keys = b'veryawesomekeyyy'

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    message = input("Encryption type: [ECB | CBC]: ... ")  # take input

    while message.lower().strip() != 'end conn':
        if message.lower().strip() == 'ecb':
            #  se trimite modul de criptare
            client_socket.send(message.encode())

            # se primeste cheia criptata
            enc_text = client_socket.recv(1024).decode()
            print('text criptat: ' + enc_text)
            temp = ECB(enc_text, key_to_decrypt_keys)

            #  se decripteaza cheia
            cheie = temp.decrypt(enc_text).encode()
            print('cheie=', cheie)

            #  poate incepe comunicarea
            client_socket.send('ready to communicate'.encode())

            #  se primeste textul criptat
            text_primit = client_socket.recv(1024).decode()
            print('text primit de la server, criptat: ', text_primit)

            # se decripteaza textul primit
            temp2 = ECB(text_primit, cheie)
            txt_decr = temp2.decrypt(text_primit)
            print('textul decriptat:', txt_decr)

        elif message.lower().strip() == 'cbc':
            #  se trimite modul de criptare
            client_socket.send(message.encode())

            # se primeste cheia criptata vectorul de initializare
            enc_text = client_socket.recv(1024).decode()
            to_rec_iv = client_socket.recv(1024).decode()
            to_rec_iv = json.loads(to_rec_iv)  # string list to list

            #  se decripteaza cheia
            temp = CBC(enc_text, key_to_decrypt_keys)
            temp.set_iv(to_rec_iv)
            cheie = temp.decrypt(enc_text).encode()
            print('cheie=', cheie)

            #  poate incepe comunicarea
            client_socket.send('my body is ready'.encode())

            #  se primeste textul criptat
            text_primit = client_socket.recv(1024).decode()
            print('text primit de la server, criptat: ', text_primit)

            # se decripteaza textul primit
            temp2 = CBC(text_primit, cheie)
            print('textul decriptat:', temp2.decrypt(text_primit))
            to_rec_iv = client_socket.recv(1024).decode()
            iv = json.loads(to_rec_iv)
            temp2.set_iv(iv)

            print('text decriptat: ', temp2.decrypt(text_primit))

        message = input(" -> ")  # again take input

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
