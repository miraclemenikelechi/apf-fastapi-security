from models import User, select, Session
from utils import verify_password


# if the authentication is by email
async def get_by_email(*, db_session: Session, mail_from_client: str) -> User | None:
    """
    Retrieves a user by their email address.

    Parameters:
    - `db_session (Session)`: The database session to use for querying.
    - `mail_from_client (str)`: The email address to search for.

    Returns:
    - `User | None`: The user object if found, otherwise None.
    """

    statement = select(User).where(User.email == mail_from_client)
    user_being_authenticated = db_session.exec(statement).first()
    return user_being_authenticated


# if the authentication is by username
async def get_by_uName(*, session: Session, uName_from_client: str) -> User | None:
    pass


async def authenticate(*, session: Session, email: str, password: str) -> User | None:
    """
    Authenticates a user based on their email and password.

    This function first retrieves the user by their email address using the `get_by_email` function.
    If the user is found, it then verifies the provided password against the stored password using the `verify_password` function.
    If both checks pass, the authenticated user object is returned. Otherwise, None is returned.

    Parameters:
    - `session (Session)`: The database session to use for querying.
    - `email (str)`: The email address of the user attempting to authenticate.
    - `password (str)`: The password provided by the user for authentication.

    Returns:
    - `User | None`: The authenticated user object if the authentication is successful, otherwise None.
    """

    user_being_authenticated = await get_by_email(
        db_session=session,
        mail_from_client=email,
    )

    if not user_being_authenticated:
        return None

    if not await verify_password(password, user_being_authenticated.password):
        return None

    return user_being_authenticated
