from datetime import timedelta
import os


# DB Configuration
DATABASE_URL = os.environ.get('SQLALCHEMY_DATABASE_URL')

API_V1_PREFIX = '/api/v1'

# JWT Configuration
JOSE = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=float(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=float(os.environ.get('REFRESH_TOKEN_EXPIRE_DAYS'))),

    'ALGORITHM': 'HS256',
    'SECRET_KEY': os.environ.get('JWT_SECRET_KEY'),
}