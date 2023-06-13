from typing import Any
from fastapi import Depends, Response
from pydantic import Field

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from . import router


class GetMyTweetsTweet(AppModel):
    id: Any = Field(alias="_id")
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str


class GetMyTweetsResponse(AppModel):
    id: Any = Field(alias="_id")
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str
    user_id: Any 


@router.get("/{tweet_id:str}", response_model=GetMyTweetsResponse)
def get_my_tweets(
    tweet_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    # user_id = jwt_data.user_id
    # tweets = svc.repository.get_tweet_by_user_id(user_id)
    the_tweet = svc.repository.get_tweet_by_user_id(tweet_id)
    if the_tweet is None:
        return Response(status_code=404, content="Tweet not found")
    return GetMyTweetsResponse(**the_tweet, content="OK")