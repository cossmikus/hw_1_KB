# modify_user.py

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from ..service import Service, get_service
from ..adapters.jwt_service import JWTData
from .dependencies import parse_jwt_user_data


class ModifyUserRequest(BaseModel):
    phone: str
    name: str
    city: str


router = APIRouter()


@router.patch("/users/me", response_model=ModifyUserRequest)
def modify_user(
    request: ModifyUserRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> ModifyUserRequest:
    user = svc.repository.get_user_by_id(jwt_data.user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    svc.repository.update_user(user_id=jwt_data.user_id, data=request.dict())

    return request
