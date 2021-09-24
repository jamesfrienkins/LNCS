from cryptography.fernet import Fernet

class cryptograph:
    def generateKey(self):
        key = Fernet.generate_key()
        with open("crypt.key", "wb") as key_file:
            key_file.write(key)

    def loadKey(self):
        return open("crypt.key", "rb").read()

    def encryptMessage(self, message):
        key = load_key()
        encoded_message = message.encode()
        f = Fernet(key)
        encrypted_message = f.encrypt(encoded_message)

        return encrypted_message

    def decryptMessage(self, encrypted_message):
        key = load_key()
        f = Fernet(key)
        decrypted_message = f.decrypt(encrypted_message)

        return decrypted_message.decode()
