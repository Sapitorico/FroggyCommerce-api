import os


class DevelopmentConfig():
    DEBUG = True
    TIMEOUT = 5


class ProductionConfig():
    DEBUG = False
    PORT = 8000


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
