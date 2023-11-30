from fastapi import FastAPI
from fastapi.routing import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from api.auth.handlers import auth_router
from api.users.handlers import user_router
from api.passwords.handlers import manager_passwords_router
import settings

app = FastAPI(title="ManagerPasswords")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

main_api_router = APIRouter()
main_api_router.include_router(user_router, prefix="/user", tags=["user"])
main_api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
main_api_router.include_router(manager_passwords_router, prefix="/passwords", tags=["passwords"])
app.include_router(main_api_router)