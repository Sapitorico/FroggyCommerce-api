import os


class DevelopmentConfig():
    DEBUG = True
    TESTING = True
    USE_RELOADER = True
    SECRET_KEY = os.getenv('SECRET_KEY')
    PREFERRED_URL_SCHEME = os.getenv('URL_SCHEME')


class ProductionConfig():
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    SERVER_NAME = os.getenv('SERVER_NAME')
    PREFERRED_URL_SCHEME = os.getenv('URL_SCHEME')


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
