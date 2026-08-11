import os
from dotenv import load_dotenv

load_dotenv()

class DevelopmentConfig: 
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    DEBUG = True
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 300
    
    
class TestingConfig:
    pass

class ProductionConfig:
    pass