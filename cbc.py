import pyaes
import numpy as np

BLOCK_SIZE = 16


def pad(text, block_size=BLOCK_SIZE):
    if len(text) % 16 is not 0:
        bytes_to_add = block_size - (len(text) % block_size)
        return text + ' ' * bytes_to_add
    return text


def pad_list(lst):
    while len(lst) % BLOCK_SIZE is not 0:
        lst.append(ord(' '))
    return lst


def xor_list(list_block, iv):
    bl = []
    for j in range(0, BLOCK_SIZE):
        bl.append(list_block[j] ^ iv[j])
    return bl


class CBC:

    def __init__(self, txt, key):
        self.key = key
        self.aes = pyaes.AES(self.key)
        self.len = len(txt)
        self.iv = list(np.random.randint(255, size=BLOCK_SIZE))

    def set_iv(self, iv):
        self.iv = iv

    def encrypt(self, txt):
        raw = pad(txt)
        ciphertext = []
        plaintext_bytes = [ord(c) for c in raw]
        iv_copy = self.iv

        for i in range(0, len(txt), BLOCK_SIZE):
            plaintext_block = plaintext_bytes[i:i + BLOCK_SIZE]
            pad_list(plaintext_block)
            xor = xor_list(plaintext_block, iv_copy)
            ciphertext += self.aes.encrypt(xor)
            iv_copy = ciphertext[i:i + BLOCK_SIZE]

        return ''.join([chr(i) for i in ciphertext])

    def decrypt(self, ciphertext):
        c = [ord(j) for j in ciphertext]
        text = []
        iv_copy = self.iv
        for i in range(0, len(c), BLOCK_SIZE):
            cipher_block = c[i:i + BLOCK_SIZE]
            pad_list(cipher_block)

            decrypt = self.aes.decrypt(cipher_block)
            xor = xor_list(iv_copy, decrypt)
            text += xor
            iv_copy = cipher_block

        return ''.join([chr(i) for i in text])[:self.len]


def test():
    msg = 'Text to test'
    cypher = CBC(msg, b'key used for CBC')

    print('plain_text:', msg)
    text_criptat = cypher.encrypt(msg)
    print('text_criptat: ', text_criptat)

    text_decriptat = cypher.decrypt(text_criptat)
    print('text_decriptat:', text_decriptat)

    if msg == text_decriptat:
        print('Successfully encrypted and decrypted.')
    else:
        print('Failed to encrypt or decrypt.')

# test()
