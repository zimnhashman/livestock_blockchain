from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os
import base64

def generate_aes_key():
    return os.urandom(32)

def encrypt_data(plaintext: str, key: bytes):
    iv = os.urandom(16)
    backend = default_backend()
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext.encode()) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(padded_data) + encryptor.finalize()

    return {
        "iv": base64.b64encode(iv).decode(),
        "ciphertext": base64.b64encode(encrypted).decode()
    }
