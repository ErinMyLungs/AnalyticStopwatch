from secrets import db_creds


class Config(object):
    pass


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{user}:{password}@{ip}:{port}/{db_name}".format(
        user=db_creds['user'],
        password=db_creds['password'],
        ip=db_creds['ip'],
        port=db_creds['port'],
        db_name=db_creds['db_name'])
    SQLALCHEMY_ECHO = True
