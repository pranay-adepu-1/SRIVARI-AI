try:
    import pytest
except ImportError:
    pytest = None
from app.security.hashing import hash_password, verify_password
from app.security.jwt import create_access_token, decode_access_token
from app.config import settings

def test_password_hashing():
    pwd = "SrivariGovindaPass!2026"
    hashed = hash_password(pwd)
    assert hashed != pwd
    assert ":" in hashed
    assert verify_password(pwd, hashed) is True
    assert verify_password("WrongPassword", hashed) is False

def test_jwt_token_creation_and_decoding():
    payload = {"sub": "user_12345", "role": "devotee"}
    token = create_access_token(payload)
    assert token is not None
    assert len(token.split('.')) == 3

    decoded = decode_access_token(token)
    assert decoded is not None
    assert decoded["sub"] == "user_12345"
    assert decoded["role"] == "devotee"
    assert "exp" in decoded

def test_jwt_invalid_token():
    assert decode_access_token("invalid.token.signature") is None
    assert decode_access_token("corrupted") is None
