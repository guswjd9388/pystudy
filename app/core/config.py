from starlette.config import Config
import pathlib

config = Config('.env')

PROJECT_NAME: str = config('PROJECT_NAME', cast=str)
VERSION: str = config('VERSION', cast=str)
DEBUG: bool = config('DEBUG', cast=bool)

DB_HOST: str = config('DB_HOST', cast=str)
DB_PORT: int = config('DB_PORT', cast=int)
DB_USER: str = config('DB_USER', cast=str)
DB_PASS: str = config('DB_PASS', cast=str)
DB_NAME: str = config('DB_NAME', cast=str)

KAKAO_REST_API_KEY: str = config('KAKAO_REST_API_KEY', cast=str)
OPEN_AI_API_KEY: str = config('OPEN_AI_API_KEY', cast=str)
