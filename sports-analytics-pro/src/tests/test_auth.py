# tests/test_auth.py
import pytest
from src.auth import hash_password, verify_password

def test_password_hashing():
    pwd = "mysecret"
    hashed = hash_password(pwd)
    assert verify_password(pwd, hashed)
    assert not verify_password("wrong", hashed)