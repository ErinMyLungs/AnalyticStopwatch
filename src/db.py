"""
This module when imported primarily is used to import Session to do database work in app.
When run standalone, it will call init_db() and create/update all tables to match models.py
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from src.config import DevConfig
from src.models import Base

#pylint: disable=C0103
engine = create_engine(DevConfig.SQLALCHEMY_DATABASE_URI)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base.query = db_session.query_property()


def init_db():
    """
    Takes models.py and will create tables from all models not already existing in db.
    :return: postgres database with models turned into tables
    """
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    init_db()
