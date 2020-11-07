import pyaes

BLOCK_SIZE = 16


def pad(text, block_size=BLOCK_SIZE):
    if len(text) % 16 is not 0:
        bytes_to_add = block_size - (len(text) % block_size)
        return text + ' ' * bytes_to_add
    return text


class ECB:

    def __init__(self, txt, key):
        self.key = key
        self.aes = pyaes.AES(self.key)
        self.len = len(txt)

    def encrypt(self, txt):
        raw = pad(txt)
        ciphertext = []
        plaintext_bytes = [ord(c) for c in raw]
        for i in range(0, len(txt), 16):
            ciphertext += self.aes.encrypt(plaintext_bytes[i:i + 16])
        return ''.join([chr(i) for i in ciphertext])

    def decrypt(self, txt):
        txt = pad(txt)
        c = [ord(j) for j in txt]
        text = []
        for i in range(0, len(c), 16):
            text += self.aes.decrypt(c[i:i + 16])
        return ''.join([chr(i) for i in text])[:self.len]


def test():
    msg = 'ana are mere'
    cypher = ECB(msg, b'best key for ecb')

    text_criptat = cypher.encrypt(msg)
    print('text_criptat: ', text_criptat)

    text_decriptat = cypher.decrypt(text_criptat)
    print('text_decriptat:', text_decriptat)

    if msg == text_decriptat:
        print('Successfully encrypted and decrypted.')
    else:
        print('Failed to encrypt or decrypt.')


# test()
