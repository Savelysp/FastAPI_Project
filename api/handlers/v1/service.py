from fastapi import APIRouter, HTTPException, Path
from fastapi.responses import ORJSONResponse
from sqlalchemy.exc import IntegrityError
from starlette import status

from src.models import Service
from src.dependencies import DBSession
from src.schemas import ServiceCreateForm, ServiceDetailForm


__all__ = [
    "router"
]

router = APIRouter()


@router.post(
    path="/service",
    status_code=status.HTTP_201_CREATED,
    response_model=ServiceDetailForm,
    response_class=ORJSONResponse
)
async def create(session: DBSession, data: ServiceCreateForm):
    # obj = Service(**data.model_dump())
    obj = Service(**data.model_dump())
    session.add(instance=obj)
    try:
        await session.commit()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="incorrect data")
    else:
        await session.refresh(instance=obj)
    return ServiceDetailForm.model_validate(obj=obj, from_attributes=True)


@router.get(
    path="/service/{pk}",
    status_code=status.HTTP_200_OK,
    response_model=ServiceDetailForm,
    response_class=ORJSONResponse
)
async def detail(
        session: DBSession,
        pk: int = Path(
            default=...,
            ge=1,
            title="Service ID",
            examples=[69]
        )
):
    obj = await session.get(
        entity=Service,
        ident=pk
    )
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return ServiceDetailForm.model_validate(obj=obj, from_attributes=True)
