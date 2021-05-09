from typing import List

from fastapi import APIRouter, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from pymongo import ReturnDocument

from app.auth import current_active_user
from app.db import movies_collection
from app.models.movies import Movie, UpdateMovie
from app.models.users import User

router = APIRouter(prefix="/movies", tags=["movies"])


@router.get("/", response_model=List[Movie])
async def get_all_movies(user: User = Depends(current_active_user)):
    movies = await movies_collection.find().to_list(1000)
    return movies


@router.get("/{id}", response_model=Movie, responses={404: {"detail": "Not Found"}})
async def get_movie(id: str):
    movie = await movies_collection.find_one({"_id": id})
    if movie:
        return movie
    else:
        raise HTTPException(status_code=404, detail=f"Movie {id} not found.")


@router.post("/", response_model=Movie, status_code=201)
async def create_movie(movie: Movie):
    movie = jsonable_encoder(movie)
    new_movie = await movies_collection.insert_one(movie)
    created_movie = await movies_collection.find_one({"_id": new_movie.inserted_id})
    return created_movie


@router.put(
    "/{id}",
    response_model=Movie,
    status_code=200,
    responses={404: {"detail": "Not Found"}},
)
async def update_movie(id: str, movie: UpdateMovie):
    update_fields = {k: v for k, v in movie.dict().items() if v is not None}

    if len(update_fields) > 0:
        update_result = await movies_collection.find_one_and_update(
            {"_id": id}, {"$set": update_fields}, return_document=ReturnDocument.AFTER
        )

        if update_result is None:
            raise HTTPException(status_code=404, detail=f"Movie {id} not found.")

        return update_result

    raise HTTPException(status_code=400, detail="Enter at least one field.")


@router.delete("/{id}", response_model=int)
async def delete_movie(id: str):
    deleted = await movies_collection.delete_one({"_id": id})
    print(deleted)
    return deleted
