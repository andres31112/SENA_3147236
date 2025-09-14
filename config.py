# config.py
class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/institucion_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'institucion_db4' 