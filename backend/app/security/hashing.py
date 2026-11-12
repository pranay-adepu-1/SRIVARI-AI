import hashlib
import os
import hmac

def hash_password(password: str) -> str:
    """
    Cryptographically secure PBKDF2-HMAC-SHA256 password hashing.
    Generates a 16-byte random salt and 100,000 iterations.
    Compatible across all environments with zero external binary dependencies.
    """
    salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt.hex() + ":" + key.hex()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a password against the stored salt + hash using constant-time comparison.
    """
    try:
        salt_hex, key_hex = hashed_password.split(":")
        salt = bytes.fromhex(salt_hex)
        key = bytes.fromhex(key_hex)
        new_key = hashlib.pbkdf2_hmac('sha256', plain_password.encode('utf-8'), salt, 100000)
        return hmac.compare_digest(key, new_key)
    except Exception:
        return False

