from src.secrets import DB_CREDS


class Config(object):
    pass


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{user}:{password}@{ip}:{port}/{db_name}".format(
        user=DB_CREDS['user'],
        password=DB_CREDS['password'],
        ip=DB_CREDS['ip'],
        port=DB_CREDS['port'],
        db_name=DB_CREDS['db_name'])
    SQLALCHEMY_ECHO = True
