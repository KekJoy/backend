from fastapi_users import FastAPIUsers

from fastapi import FastAPI, Depends
from fastapi_users import FastAPIUsers

from auth.auth import auth_backend
from auth.models.db import User
from auth.models.schemas import UserRead, UserCreate
from auth.services.user import get_user_manager

app = FastAPI(
    title="Система внешнего обучения"
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

current_user = fastapi_users.current_user()


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.name}"


@app.get("/unprotected-route")
def unprotected_route():
    return f"Hello, anonym"
