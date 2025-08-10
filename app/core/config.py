from typing import Optional

from pydantic import EmailStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Aplication QRKot'
    description: str
    database_url: str
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    jwt_token_lifetime: int
    user_password_min_len: int
    logging_format: str = '%(asctime)s - %(levelname)s - %(message)s'
    logging_dt_format: str = '%Y-%m-%d %H:%M:%S'

    class Config:
        env_file = '.env'


settings = Settings()


class Constants:
    JWT_TOKEN_URL = 'auth/jwt/login'
    JWT_AUTH_BACKEND_NAME = 'jwt'
    NAME_MIN_LEN = 1
    NAME_MAX_LEN = 100
    PROJECT_ENDPOINTS_PREFIX = '/charity_project'
    PROJECT_ENDPOINTS_TAGS = ('charity_projects',)
    DONATION_ENDPOINTS_PREFIX = '/donation'
    DONATION_ENDPOINTS_TAGS = ('donations',)


class Messages:
    PASSWORD_TOO_SHORT = (
        f'Password must be not less {settings.user_password_min_len}'
    )
    EMAIL_IN_PASSWORD = 'Password should`t contain email'
    USER_REGISTERED = 'User registered: '
    INVESTMENT_ERROR = 'An error has occurred during investment'
    PROJECT_AMOUNTS_ERROR = (
        'Full amount cannot be less than already '
        'invested amount'
    )
    PROJECT_FUTURE_DATE_ERROR = 'Project open date cannoy be at future'
    PROJECT_NAME_OCCUPIED = 'Project name already exist'
    PROJECT_NAME_NOT_NULL = 'Project name cannot be empty'
    PROJECT_DESCRIPTION_NOT_NULL = 'Project description cannot be empty'
    PROJECT_NOT_FOUND = 'Project with given ID not found'
    PROJECT_INVESTED = 'Project was already invested, cannot delete'
    PROJECT_CLOSED = 'Closed project cannot be edited'