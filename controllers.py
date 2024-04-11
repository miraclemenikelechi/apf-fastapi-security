from datetime import timedelta

from fastapi import HTTPException

from config import server_config
from crud import authenticate
from dependencies import AUTH_REQUEST_DEPENDENCY, SESSION_DEPENDENCY
from models import Token, User, select
from utils import create_access_token, handle_firebase_phonenumber, hash_password


async def register_new_user(
    data_from_client: dict,
    invoke_database: SESSION_DEPENDENCY,
) -> User:

    try:

        # check if user exists in database
        user_exists = invoke_database.exec(
            select(User).where(User.email == data_from_client.email)
        ).first()

        if user_exists:
            raise HTTPException(
                status_code=400,
                detail="User with that email already exists",
            )

        # create a new user dictionary
        created_user: User = {
            "name": data_from_client.name,
            "age": data_from_client.age,
            "phone": await handle_firebase_phonenumber(data_from_client.phone),
            "email": data_from_client.email,
            "password": await hash_password(data_from_client.password),
        }

        # created user in DB
        created_user_in_db = User(**created_user)

        # add to database
        invoke_database.add(created_user_in_db)
        invoke_database.commit()
        invoke_database.refresh(created_user_in_db)

        return created_user

    except HTTPException as error:
        raise error


async def log_users_into_system(
    data_from_client: dict,
    invoke_database: SESSION_DEPENDENCY,
) -> Token:

    # auth with email
    user = await authenticate(
        email=data_from_client.email,
        password=data_from_client.password,
        session=invoke_database,
    )

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid email or password",
        )

    access_token_expiration = timedelta(minutes=server_config.VALID_TOKEN_IN_MINUTES)

    return Token(
        access_token=await create_access_token(
            subject_to_encode=user.id,
            expiration_time_delta=access_token_expiration,
        )
    )
