class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:*D3tr01t26!*@localhost/mechanic_api'
    DEBUG = True
    
    
class TestingConfig:
    pass

class ProductionConfig:
    pass