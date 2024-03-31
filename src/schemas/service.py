from decimal import Decimal

from pydantic import Field, PositiveInt

from .base import Schema

__all__ = [
    "ServiceCreateForm",
    "ServiceEditForm",
    "ServiceDetailForm"
]


class ServiceCreateForm(Schema):
    name: str = Field(
        default=...,
        title="Name",
        examples=["Vasya"],
    )
    price: Decimal = Field(
        default=...,
        title="Price",
        examples=[34.34],
        gt=0,
        decimal_places=2
    )
    title: str = Field(
        default=...,
        title="Some title",
    )


class ServiceEditForm(ServiceCreateForm):
    ...


class ServiceDetailForm(ServiceCreateForm):
    id: PositiveInt = Field(
        default=...,
        title="Service ID",
    )
