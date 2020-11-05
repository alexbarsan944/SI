import pyaes


def pad(text, block_size=16):
    bytes_to_add = block_size - (len(text) % block_size)
    return text + chr(bytes_to_add) * bytes_to_add


class ECB:

    def __init__(self, txt):
        self.key = b'1234567890123456'
        self.aes = pyaes.AES(self.key)
        self.len = len(txt)

    def encrypt(self, txt):
        raw = pad(txt)
        ciphertext = []
        plaintext_bytes = [ord(c) for c in raw]
        for i in range(0, len(plaintext_bytes), 16):
            ciphertext += self.aes.encrypt(plaintext_bytes[:16])
            plaintext_bytes = plaintext_bytes[16:]
        return ''.join([chr(i) for i in ciphertext])

    def decrypt(self, ciphertext):
        c = [ord(j) for j in ciphertext]
        text = []
        for i in range(0, len(c), 16):
            text += self.aes.decrypt(c[:16])
            c = c[16:]
        return ''.join([chr(i) for i in text])[:self.len]


def test():
    msg = input('Plaintext: ')
    cypher = ECB(msg)

    text_criptat = cypher.encrypt(msg)
    print('text_criptat: ', text_criptat)

    text_decriptat = cypher.decrypt(text_criptat)
    print('text_decriptat:', text_decriptat)

    print(msg == text_decriptat)


test()
