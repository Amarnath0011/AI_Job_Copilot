import pytest

from app import core
from app.core import security


def test_password_hash_verifies_without_storing_plaintext():
    password = "StrongPassword123!"
    hashed = security.hash_password(password)

    assert hashed != password
    assert security.verify_password(password, hashed)
    assert not security.verify_password("wrong-password", hashed)


def test_jwt_round_trip(monkeypatch):
    monkeypatch.setattr(security, "JWT_SECRET_KEY", "test-secret-that-is-long-enough-for-jwt-tests-123")
    token = security.create_access_token(42)

    assert security.decode_access_token(token) == 42


def test_invalid_jwt_is_rejected(monkeypatch):
    monkeypatch.setattr(security, "JWT_SECRET_KEY", "test-secret-that-is-long-enough-for-jwt-tests-123")

    with pytest.raises(ValueError, match="Invalid or expired"):
        security.decode_access_token("not-a-valid-token")


def test_missing_jwt_secret_fails_closed(monkeypatch):
    monkeypatch.setattr(security, "JWT_SECRET_KEY", None)

    with pytest.raises(RuntimeError, match="JWT_SECRET_KEY"):
        security.create_access_token(1)
