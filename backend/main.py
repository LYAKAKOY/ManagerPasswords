from fastapi import FastAPI
from fastapi.routing import APIRouter

from api.auth.handlers import auth_router
from api.users.handlers import user_router
from api.passwords.handlers import manager_passwords_router

app = FastAPI(title="ManagerPasswords")

main_api_router = APIRouter()
main_api_router.include_router(user_router, prefix="/user", tags=["user"])
main_api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
main_api_router.include_router(manager_passwords_router, prefix="/passwords", tags=["passwords"])
app.include_router(main_api_router)