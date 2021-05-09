from fastapi import FastAPI

from app.auth import auth_router, user_router
from app.routers import movies

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "ok"}


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(movies.router)
