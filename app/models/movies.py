from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional

from app.models.mongo import PyObjectId


class Movie(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    rating: float

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}


class UpdateMovie(BaseModel):
    name: Optional[str]
    rating: Optional[float]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
