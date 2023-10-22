from app.api.api_routes import all_routes
from app.api import home
from app.core.config import PROJECT_NAME, DEBUG, VERSION
from app.core import handlers
from fastapi import FastAPI, HTTPException


def get_application() -> FastAPI:
    application = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)
    application.add_exception_handler(
        HTTPException, handlers.http_error_handler)
    application.include_router(all_routes, prefix='/api')
    application.include_router(home.router)
    return application


app = get_application()
