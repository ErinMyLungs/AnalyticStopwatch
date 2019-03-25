#TODO: Kill if not actually used

from config import DevConfig
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
"""
Possibly Outmoded by  flask-sqlalchemy
"""
engine = create_engine(DevConfig.SQLALCHEMY_DATABASE_URI)
Session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=engine))
