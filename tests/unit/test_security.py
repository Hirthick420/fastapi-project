# tests/unit/test_security.py
from app.core.security import get_password_hash, verify_password

def test_password_hash_and_verify():
    password = "mysecretpassword"
    hash_1 = get_password_hash(password)
    hash_2 = get_password_hash(password)

    assert hash_1 != hash_2  # bcrypt hashes are salted
    assert verify_password(password, hash_1)
    assert verify_password(password, hash_2)
    assert not verify_password("wrongpassword", hash_1)
