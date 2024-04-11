from typing import Annotated, Generator

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from config import server_config
from database import engine
from models import AuthRequest, Session, User
from utils import verify_access_token


def db_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


set_token_url: str = f"{server_config.CURRENT_API_URL}/login"
get_oauth2_token: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl=set_token_url)

SESSION_DEPENDENCY = Annotated[Session, Depends(db_session)]
TOKEN_DEPENDENCY = Annotated[str, Depends(get_oauth2_token)]


def get_current_user(session: SESSION_DEPENDENCY, token: TOKEN_DEPENDENCY):
    token_data = verify_access_token(token)
    user = session.get(User, token_data.subject_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


CURRENT_USER_DEPENDENCY = Annotated[User, Depends(get_current_user)]
AUTH_REQUEST_DEPENDENCY = Annotated[AuthRequest, Depends()]
