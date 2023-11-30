import os

from cryptography.fernet import Fernet


class AES:
    cipher_suite = Fernet(os.environ.get("AES_KEY").encode("utf-8"))

    @classmethod
    def encrypt_password(cls, password: str) -> bytes:
        password_bytes = password.encode("utf-8")
        return cls.cipher_suite.encrypt(password_bytes)

    @classmethod
    def decrypt_password(cls, password: bytes) -> str:
        password_bytes = cls.cipher_suite.decrypt(password)
        return password_bytes.decode("utf-8")
