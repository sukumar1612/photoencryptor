import pyaes, pbkdf2, binascii, os, secrets
from bitstring import BitArray

class AESCipher:
    iv = 97258264557740063406268630518792288178031654452768031515803456860648001468651
    passwordSalt = b'f\x93\xf0\x9dH\x96\xdab\xb7R_\xf0W\xab\xc82'

    def __init__(self, password):
        self.key = pbkdf2.PBKDF2(password, self.passwordSalt).read(32)
        self.aes = pyaes.AESModeOfOperationCTR(self.key, pyaes.Counter(self.iv))

    def encrypt(self, text):
        aes = pyaes.AESModeOfOperationCTR(self.key, pyaes.Counter(self.iv))
        ciphertext = aes.encrypt(text)
        return binascii.hexlify(ciphertext).decode("utf-8")

    def decrypt(self, text):
        text = binascii.unhexlify(text.encode("utf-8"))
        aes = pyaes.AESModeOfOperationCTR(self.key, pyaes.Counter(self.iv))
        decrypted = aes.decrypt(text)
        return decrypted.decode("utf-8")
