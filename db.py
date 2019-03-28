from config import DevConfig
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import Base

engine = create_engine(DevConfig.SQLALCHEMY_DATABASE_URI)
Session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=engine))
Base.query = Session.query_property()


def init_db():
    """
    Takes models.py and will create tables from all models not already existing in db.
    :return: postgres database with models turned into tables
    """
    import models
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    init_db()
