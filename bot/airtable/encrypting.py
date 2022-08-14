from cryptography.fernet import Fernet

from bot.config import ENC_KEY

key = Fernet(bytes(ENC_KEY, 'UTF-8'))




def encrypt_password(unsecured_data: str):
    password = unsecured_data
    enc_password = key.encrypt(password.encode())
    return enc_password


def decrypt_password(secured_data: bytes):
    password = secured_data
    dec_password = key.decrypt(password).decode()
    return dec_password


