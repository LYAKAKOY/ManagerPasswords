from cryptography.fernet import Fernet


class AES:
    __slots__ = ["cipher_suite"]

    def __init__(self, aes_key: bytes):
        self.cipher_suite = Fernet(aes_key)

    def encrypt_password(self, password: str) -> bytes:
        password_bytes = password.encode("utf-8")
        return self.cipher_suite.encrypt(password_bytes)

    def decrypt_password(self, password: bytes) -> str:
        password_bytes = self.cipher_suite.decrypt(password)
        return password_bytes.decode("utf-8")
