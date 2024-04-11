from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from controllers import log_users_into_system, register_new_user
from dependencies import (
    AUTH_REQUEST_DEPENDENCY,
    CURRENT_USER_DEPENDENCY,
    SESSION_DEPENDENCY,
)
from models import CreateUser, ReadUser

users = APIRouter(prefix="/users", tags=["authentication"])


@users.post("/new")
async def register_user(user: CreateUser, db_access: SESSION_DEPENDENCY):

    data = await register_new_user(
        data_from_client=user,
        invoke_database=db_access,
    )

    if not data:
        raise HTTPException(
            status_code=400,
            detail="user registration failed!",
        )

    response = {
        "message": "user created successfully",
        "data": jsonable_encoder(data),
    }

    return JSONResponse(content=response, status_code=201)


@users.post("/login")
async def users_login(
    form_data: AUTH_REQUEST_DEPENDENCY, db_access: SESSION_DEPENDENCY
):

    data = await log_users_into_system(
        data_from_client=form_data,
        invoke_database=db_access,
    )

    if not data:
        raise HTTPException(
            status_code=401,
            detail="user login failed!",
        )

    response = {
        "message": "user logged in successfully",
        "data": jsonable_encoder(data),
    }

    return JSONResponse(content=response, status_code=200)


@users.post("/confirm_token", response_model=ReadUser)
async def test_token(user_trying_to_sign_in: CURRENT_USER_DEPENDENCY) -> Any:
    return user_trying_to_sign_in
