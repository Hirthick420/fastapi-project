from app.core.security import get_password_hash, verify_password


def test_password_change_hash_and_verify():
    old_password = "oldpass123"
    new_password = "newpass456"

    old_hash = get_password_hash(old_password)
    new_hash = get_password_hash(new_password)

    assert verify_password(old_password, old_hash)
    assert not verify_password(old_password, new_hash)
    assert verify_password(new_password, new_hash)
