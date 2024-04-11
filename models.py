import re
from typing import Annotated
from uuid import UUID, uuid4

from fastapi import Form, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import AfterValidator, EmailStr, PositiveInt, ValidationError
from pydantic.dataclasses import dataclass
from pydantic_extra_types.phone_numbers import PhoneNumber
from sqlmodel import VARCHAR, Column, Field, Session, SQLModel, select


def validate_password(value: str) -> str:
    """
    Validates the password value against a regex pattern to ensure it meets the expected criteria.

    Args:
    - `cls (class)`: The class object.
    - `value (str)`: The password value to be validated.

    Raises:
    - `HTTPException`: If the password value does not meet the expected criteria.

    Returns:
    - `str`: The validated password value.
    """

    regex_pattern: str = r"((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,64})"

    if not re.match(regex_pattern, value):
        raise HTTPException(
            status_code=422,
            detail="password does not meet the expected criteria",
        )

    return value


class BaseUser(SQLModel):
    name: str = Field(
        title="name",
        description="The user's full name.",
        min_length=3,
        max_length=150,
    )

    age: PositiveInt = Field(
        title="age",
        default=None,
        gt=0,
        description="The user's age in years.",
    )

    phone: PhoneNumber = Field(
        title="phone number",
        description="The user's phone number.",
    )

    email: EmailStr = Field(
        title="email",
        sa_column=Column(
            "email",
            VARCHAR,
            unique=True,
            index=True,
        ),
        description="The user's email address.",
    )


class CreateUser(BaseUser):
    password: Annotated[
        str,
        Field(
            min_length=8,
            max_length=100,
            description="The user's password.",
        ),
        AfterValidator(validate_password),
    ]


class ReadUser(BaseUser):
    id: UUID


@dataclass
class AuthRequest(OAuth2PasswordRequestForm):
    email: EmailStr = Form()
    password: str = Form()


class User(CreateUser, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)


# must be sub? idk why
# content of jwt
class TokenID(SQLModel):
    subject_id: str | None = None


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"
