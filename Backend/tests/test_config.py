import pytest
from pydantic import ValidationError

from app.core.config import Settings


def test_settings_rejects_short_jwt_secret_key():
    with pytest.raises(ValidationError, match="al menos 32 caracteres"):
        Settings(
            database_url="sqlite:///./test.db",
            jwt_secret_key="clave-corta"
        )


def test_settings_accepts_valid_jwt_secret_key():
    settings = Settings(
        database_url="sqlite:///./test.db",
        jwt_secret_key="a" * 32
    )

    assert settings.access_token_expire_minutes == 15
