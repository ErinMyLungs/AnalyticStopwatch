from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(255))
    password = Column(String(255))

    posts = relationship("Post", back_populates="User", lazy='dynamic')

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return "<User '{}'>".format(self.username)


class Post(Base):
    __tablename__ = 'Post'
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    text = Column(Text)
    publish_date = Column(DateTime)
    user_id = Column(Integer, ForeignKey('user.id'))

    user = relationship("user", back_populates="post")

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return "<Post '{title}'>".format(title=self.title)
