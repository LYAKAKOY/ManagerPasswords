from fastapi import FastAPI
from fastapi.routing import APIRouter

from api.auth.handlers import auth_router
from api.users.handlers import user_router

app = FastAPI(title="ManagerPasswords")

main_api_router = APIRouter()
main_api_router.include_router(user_router, prefix="/user", tags=["user"])
main_api_router.include_router(auth_router, prefix="/login", tags=["login"])
app.include_router(main_api_router)