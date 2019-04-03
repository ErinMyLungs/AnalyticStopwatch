#pylint: disable:R0903
"""SQLAlchemy table models and declarative_base."""
import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """Linked with Post table"""
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False, unique=True)
    password = Column(String(255))

    posts = relationship("Post", back_populates="User", lazy='dynamic')

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return "<User '{}'>".format(self.username)


class Post(Base):
    """Linked to User, Comments, and Tag tables."""
    __tablename__ = 'Post'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    text = Column(Text)
    publish_date = Column(DateTime, default=datetime.datetime.now)
    user_id = Column(Integer, ForeignKey('user.id'))

    user = relationship(
        "user",
        back_populates="post")

    comment = relationship(
        "comment",
        backref="post",
        lazy='dynamic')

    tags = relationship(
        "Tag",
        backref="post",
        lazy="dynamic")

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return "<Post '{title}'>".format(title=self.title)


class Comment(Base):
    """Connected to Post table. Should possibly be connected to User"""
    __tablename__ = 'Comment'
    id = Column(Integer(), primary_key=True)
    name = Column(String(255), nullable=False)
    text = Column(Text())
    date = Column(DateTime, default=datetime.datetime.now)
    post_id = Column(Integer(), ForeignKey('Post.id'))

    def __repr__(self):
        return "<Comment '{}'>".format(self.text[:15])


class Tag(Base):
    """One-to-many to individual posts"""
    __tablename__ = 'Tag'
    id = Column(Integer(), primary_key=True)
    title = Column(String(255), nullable=False)

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return "<Tag '{}'>".format(self.title)
