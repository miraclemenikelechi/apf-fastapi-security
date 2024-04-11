import secrets
from typing import Annotated, Literal

from pydantic import AnyUrl, BeforeValidator
from pydantic_settings import BaseSettings, SettingsConfigDict
from passlib.context import CryptContext


def parse_server(value: any) -> str | list[str]:
    """
    Parses a server value into a list of strings.

    Args:
    - `value (any)`: The server value to parse. This can be a string or a list.

    Returns:
    - `str | list[str]`: A list of strings representing the server or servers.

    Raises:
    - `ValueError`: If the server value is invalid.
    """

    if isinstance(value, str) and not value.startswith("["):
        return [item_in_list.strip() for item_in_list in value.split(",")]

    elif isinstance(value, list | str):
        return value

    raise ValueError(f"Invalid server value: {value}")


class AppSettings(BaseSettings):
    model_config: SettingsConfigDict = {
        "extra": "ignore",
        "env_file": ".env",
        "env_ignore_empty": True,
    }

    ALGORITHM: str = "HS256"

    CURRENT_API_URL: str = "/api/v1"

    SECRET_KEY: str = secrets.token_urlsafe(32)

    # 60 minutes * 24 hours * 8 days = 8 days
    VALID_TOKEN_IN_MINUTES: int = 60 * 24 * 8

    DOMAIN: str = "localhost"

    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_server)
    ] = []

    PASSWORD_CONTEXT: CryptContext = CryptContext(
        schemes=["bcrypt"],
        deprecated="auto",
    )


server_config: AppSettings = AppSettings()
