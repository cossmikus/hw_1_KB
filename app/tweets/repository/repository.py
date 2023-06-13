from typing import Any
from bson.objectid import ObjectId
from pymongo.database import Database
from pymongo.results import UpdateResult, DeleteResult


class TweetRepository:
    
    def __init__(self, database: Database):
        self.database = database

    def create_tweet_rep(self, user_id: str, data: dict[str, Any]):
        data["user_id"] = ObjectId(user_id)
        insert_to_the_db = self.database["tweets"].insert_one(data)
        return insert_to_the_db.inserted_id

    def get_tweet_by_user_id(self, tweet_id: str):
        return self.database["tweets"].find_one({"_id": ObjectId(tweet_id)})
    
    def update_tweet_info(self, tweet_id: str, 
                          user_id: str, data: dict[str, Any]) -> UpdateResult:
        return self.database["tweets"].update_one(
            filter={"_id": ObjectId(tweet_id), "user_id": ObjectId(user_id)},
            update={"$set": data},
        )
        
    def delete_tweet_info(self, tweet_id: str, 
                          user_id: str) -> DeleteResult:
        return self.database["tweets"].delete_one(
            {"_id": ObjectId(tweet_id), "user_id": ObjectId(user_id)}
        )

