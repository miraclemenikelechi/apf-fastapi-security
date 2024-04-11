from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt

from config import server_config
from models import TokenID, ValidationError


async def handle_firebase_phonenumber(value: str) -> str:
    phone_number = "".join(item for item in value if item.isdigit())
    return f"+{phone_number}"


async def hash_password(password: str) -> str:
    return server_config.PASSWORD_CONTEXT.hash(password)


async def verify_password(password: str, hashed_password: str) -> bool:
    return server_config.PASSWORD_CONTEXT.verify(password, hashed_password)


# subject_to_encode is what we want to encode, expiration_time_delta is how long the token should last
async def create_access_token(
    subject_to_encode: str | Any,
    expiration_time_delta: timedelta,
) -> str:

    # get server timezone
    expiration_time = datetime.now(timezone.utc) + expiration_time_delta

    created_access_token = jwt.encode(
        claims={"exp": expiration_time, "subject_id": str(subject_to_encode)},
        key=server_config.SECRET_KEY,
        algorithm=server_config.ALGORITHM,
    )

    return created_access_token


def verify_access_token(token_from_client: str):
    try:
        payload = jwt.decode(
            token=token_from_client,
            key=server_config.SECRET_KEY,
            algorithms=[server_config.ALGORITHM],
        )

        token_data = TokenID(**payload)

    except (JWTError, ValidationError) as error:
        raise error

    return token_data
