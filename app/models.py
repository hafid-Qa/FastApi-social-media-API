from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

# to create associations
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, nullable=False, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"), onupdate=text("now()"))
    posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="True", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"), onupdate=text("now()"))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="posts")
