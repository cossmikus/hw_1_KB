from fastapi import Depends, Response

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from . import router


class UpdateMyTweetsTweet(AppModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str


@router.delete("/{tweet_id:str}")
def delete_my_tweet(
    tweet_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    # user_id = jwt_data.user_id
    delete_temp = svc.repository.delete_tweet_info(
        tweet_id, jwt_data.user_id
    )
    
    if delete_temp.deleted_count == 1:
        return Response(status_code=200, content="OK")
    return Response(status_code=404)
