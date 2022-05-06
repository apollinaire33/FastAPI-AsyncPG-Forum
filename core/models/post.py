from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from db.database import Base


class PostCategory(Base):
    __tablename__ = 'post_categories'

    id = Column(Integer, primary_key=True, autoincrement='auto', index=True)
    title = Column(String(25), nullable=False, unique=True)
    description = Column(String(100))
    posts = relationship('Post')

    def __repr__(self):
        return self.title


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement='auto', index=True)
    title = Column(String(100), nullable=False)
    text = Column(Text)
    time_created = Column(DateTime(timezone=True), default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    category = Column(String, ForeignKey('post_categories.title'), nullable=False)

    def __repr__(self):
        return self.title
