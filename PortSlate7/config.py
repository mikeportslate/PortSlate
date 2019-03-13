from os import environ


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_RECYCLE = 3600
    SQLALCHEMY_ECHO=True

    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'CTaUlI2kbIe9GFA9jI2Hz9krZRZzF0wEW0Tw7kqf'


class ProductionConfig(Config):
    DEBUG = False

    # PostgreSQL database
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
        environ.get('PORTSLATE_DATABASE_USER', 'mikelam'),
        environ.get('PORTSLATE_DATABASE_PASSWORD', '12345678'),
        environ.get('PORTSLATE_DATABASE_HOST', 'awssample1.cji0zdy5khnh.us-west-2.rds.amazonaws.com'),
        environ.get('PORTSLATE_DATABASE_PORT', 3306),
        environ.get('PORTSLATE_DATABASE_NAME', 'PortSlate')
    )


class DebugConfig(Config):
    DEBUG = True


config_dict = {
    'Production': ProductionConfig,
    'Debug': DebugConfig
}
