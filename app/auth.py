from fastapi import APIRouter
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication

from app.db import user_db
from app.models.users import User, UserCreate, UserUpdate, UserDB

SECRET = "SECRET"
auth_backends = []
jwt_authentication = JWTAuthentication(secret=SECRET, lifetime_seconds=3600)
auth_backends.append(jwt_authentication)

fastapi_users = FastAPIUsers(
    user_db,
    auth_backends,
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)

current_active_user = fastapi_users.current_user(active=True)

auth_router = APIRouter(tags=["auth"])

auth_router.include_router(
    fastapi_users.get_auth_router(jwt_authentication, requires_verification=False)
)
auth_router.include_router(fastapi_users.get_register_router())

user_router = APIRouter(tags=["users"])

user_router.include_router(
    fastapi_users.get_users_router(),
    prefix="/users",
)
