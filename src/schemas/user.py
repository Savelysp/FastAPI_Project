from typing import Self

from pydantic import EmailStr, model_validator, Field, PositiveInt

from .base import Schema
from .types import PasswordStr

__all__ = [
    "UserRegisterForm",
    "UserLoginForm",
    "UserDetail"
]


class UserRegisterForm(Schema):
    email: EmailStr = Field(
        default=...,
        title="User email",
        examples=["you@yourdomain.com"]
    )
    password: PasswordStr = Field(
        default=...,
        title="Password",
        examples=["VeryStrongPassword1!"]
    )
    confirm_password: PasswordStr = Field(
        default=...,
        title="Confirm Password",
        examples=["VeryStrongPassword1!"]
    )

    @model_validator(mode="after")
    def validator(self) -> Self:
        if self.password != self.confirm_password:
            raise ValueError("not match")

        return self


class UserLoginForm(Schema):
    email: EmailStr = Field(
        default=...,
        title="User email",
        examples=["you@yourdomain.com"]
    )
    password: PasswordStr = Field(
        default=...,
        title="Password",
        examples=["VeryStrongPassword1!"]
    )


class UserDetail(Schema):
    id: PositiveInt = Field(
        default=...,
        title="User ID",
        examples=[12345]
    )
    email: EmailStr = Field(
        default=...,
        title="User email",
        examples=["you@yourdomain.com"]
    )
