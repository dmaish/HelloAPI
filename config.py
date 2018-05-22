import os


class Config(object):
    """common configurations that are common across all environments"""

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_ECHO = True
    DEBUG = True


class DevelopmentConfig(Config):
    """Development configurations"""
#  should time to use a database come this will be the
#  perfect place to put all the configurations


class ProductionConfig(Config):
    """production configurations"""
    SQLALCHEMY_ECHO = False
    DEBUG = False


class TestingConfig(Config):
    """ Testing configurations """
    SQLALCHEMY_DATABASE_URI = 'postgresql:///test_hello_books_db'
    TESTING = True


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
    }