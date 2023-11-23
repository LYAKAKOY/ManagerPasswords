from fastapi import FastAPI
from fastapi.routing import APIRouter

app = FastAPI(title="ManagerPassword")

main_api_router = APIRouter()

app.include_router(main_api_router)