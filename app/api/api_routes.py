from app.api import auth, batch
from fastapi import APIRouter

all_routes = APIRouter()
all_routes.include_router(auth.router, tags=['auth'], prefix='/auth')
all_routes.include_router(batch.router, tags=['batch'], prefix='/batch')
