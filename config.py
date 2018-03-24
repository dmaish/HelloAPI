class Config(object):
    """common configurations that are common across all environments"""

    DEBUG = True


class DevelopmentConfig(Config):
    """Development configurations"""
#  should time to use a database come this will be the
#  perfect place to put all the configurations


class ProductionConfig(Config):
    """production configurations"""

    DEBUG = False


class TestingConfig(Config):
    """ Testing configurations """
    TESTING = True


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
    }