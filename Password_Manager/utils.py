import secrets
import string
from flask import current_app
from werkzeug.security import check_password_hash, generate_password_hash
from cryptography.fernet import Fernet


def hash_password(password):
    return generate_password_hash(password)


def verify_password(password_hash, password):
    return check_password_hash(password_hash, password)


def get_fernet():
    key = current_app.config.get("FERNET_KEY")
    if isinstance(key, str):
        key = key.encode("utf-8")
    return Fernet(key)


def encrypt_password(plain_password):
    return get_fernet().encrypt(plain_password.encode("utf-8")).decode("utf-8")


def decrypt_password(encrypted_password):
    return get_fernet().decrypt(encrypted_password.encode("utf-8")).decode("utf-8")


def generate_password(length=16, use_uppercase=True, use_lowercase=True, use_numbers=True, use_symbols=True):
    if not 8 <= length <= 32:
        raise ValueError("Password length must be between 8 and 32 characters.")

    characters = ""
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_numbers:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    if not characters:
        raise ValueError("At least one character type must be selected.")

    return "".join(secrets.choice(characters) for _ in range(length))
