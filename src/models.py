import os
import sys
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, Enum
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String, nullable=False)
    lastname: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    
    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="author")
    followers = relationship("Follower", foreign_keys="[Follower.user_from_id]", back_populates="follower")
    following = relationship("Follower", foreign_keys="[Follower.user_to_id]", back_populates="followed")

class Post(Base):
    __tablename__ = 'post'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    
    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    media = relationship("Media", back_populates="post")

class Comment(Base):
    __tablename__ = 'comment'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    comment_text: Mapped[str] = mapped_column(String, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)
    
    author = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

class Media(Base):
    __tablename__ = 'media'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str] = mapped_column(Enum("image", "video", name="media_type"), nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)
    
    post = relationship("Post", back_populates="media")

class Follower(Base):
    __tablename__ = 'follower'
    
    user_from_id: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key=True)
    user_to_id: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key=True)
    
    follower = relationship("User", foreign_keys=[user_from_id], back_populates="followers")
    followed = relationship("User", foreign_keys=[user_to_id], back_populates="following")

# Generar el diagrama
try:
    result = render_er(Base, 'diagram.png')
    print("¡Éxito! Revisa el archivo diagram.png")
except Exception as e:
    print("Hubo un problema al generar el diagrama")
    raise e