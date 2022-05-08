from passlib.hash import pbkdf2_sha256
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum
from sqlalchemy.sql import func

from db.database import Base
from services.enums import RolesEnum


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement='auto', index=True)
    username = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    password = Column(String(128), nullable=False)
    
    role = Column(
        Enum(RolesEnum, values_callable=lambda obj: [e.value for e in obj]),
        server_default=RolesEnum.USER.value, 
        nullable=False
    )
    date_joined = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    active = Column(Boolean, nullable=False, server_default='true')
    
    __mapper_args__ = {"eager_defaults": True}

    def __init__(self, username, password, email) -> None:
        self.username = username
        self.email = email
        self.password = pbkdf2_sha256.encrypt(password)

    def verify_password(self, password: str) -> bool:
        return pbkdf2_sha256.verify(password, self.password)

    def __repr__(self):
        return self.username
