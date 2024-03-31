from fastapi import FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from starlette import status

from src.dependencies import DBSession
from src.models import User
from src.schemas import UserDetail, UserRegisterForm, TokenPairDetail, UserLoginForm, TokenRefreshForm
from src.settings import settings
from src.utils import create_password_hash, password_verify, create_access_token, create_refresh_token, \
    verify_refresh_token

app = FastAPI(
    docs_url="/auth/docs",
    redoc_url="/auth/redoc",
    openapi_url="/auth/openapi.json"
)


@app.post(
    path="/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserDetail
)
async def register(session: DBSession, data: UserRegisterForm):
    user = User(
        **data.model_dump(exclude={"confirm_password"}) | {
            "password": create_password_hash(password=data.password)
        }
    )
    session.add(instance=user)
    try:
        await session.commit()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email exist")
    else:
        await session.refresh(instance=user)
    return UserDetail.model_validate(obj=user, from_attributes=True)


@app.post(
    path="/login",
    status_code=status.HTTP_200_OK,
    response_model=TokenPairDetail
)
async def login(session: DBSession, data: UserLoginForm):
    user = await session.scalar(
        select(User).filter(User.email == data.email)
    )
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user not found")

    if password_verify(password=data.password, password_hash=user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="password is incorrect")

    payload = {
        "sub": user.id
    }
    access_token = create_access_token(payload=payload)
    refresh_token = create_refresh_token(payload=payload)
    return TokenPairDetail(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type=settings.TOKEN_TYPE,
        expire=settings.JWT_ACCESS_EXP
    )


@app.post(
    path="/refresh",
    response_model=TokenPairDetail,
    status_code=status.HTTP_200_OK
)
async def refresh(data: TokenRefreshForm):
    try:
        payload = verify_refresh_token(jwt=data.refresh_token)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")

    payload = {
        "sub": payload.get("sub")
    }
    access_token = create_access_token(payload=payload)
    refresh_token = create_refresh_token(payload=payload)
    return TokenPairDetail(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type=settings.TOKEN_TYPE,
        expire=settings.JWT_ACCESS_EXP
    )


if __name__ == '__main__':
    from uvicorn import run
    run(
        app=app,
        host="0.0.0.0",
        port=80
    )
